"""Reproducible, assumption-based 3-D lid elasticity and mesh-refinement study.

Units throughout the solve: mm, N, MPa (N/mm^2).
Gmsh imports actual STEP geometry; scikit-fem assembles quadratic displacement
tetrahedra over straight-sided tetrahedral geometric cells. No synthetic results.
"""
from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path

import gmsh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.tri as mtri
import meshio
import numpy as np
from skfem import Basis, MeshTet, ElementTetP2, ElementVector, LinearForm, asm, condense, solve
from skfem.models.elasticity import lame_parameters, linear_elasticity

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
PLOTS = OUT / "plots"
MESHES = OUT / "meshes"
ELEMENT = ElementVector(ElementTetP2())
CONFIG = json.loads((HERE / "study.json").read_text())
COLORS = {"navy": "#14364a", "teal": "#087f8c", "amber": "#d68619", "red": "#c44d43"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titleweight": "bold", "figure.facecolor": "white"})


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_configuration():
    if CONFIG["youngs_modulus_mpa"] <= 0 or not -1 < CONFIG["poisson_ratio"] < .5:
        raise ValueError("Elastic modulus must be positive and Poisson ratio must lie between -1 and 0.5")
    if CONFIG["total_downward_force_n"] <= 0:
        raise ValueError("The specified downward force must be positive")
    sizes = CONFIG["mesh_sizes_mm"]
    if len(sizes) < 3 or any(x <= 0 for x in sizes) or any(a <= b for a, b in zip(sizes, sizes[1:])):
        raise ValueError("Supply at least three strictly decreasing positive mesh sizes")
    if not 0 < CONFIG["stress_probe_depth_fraction"] < 1:
        raise ValueError("Stress probe depth fraction must lie inside the lid")
    if not 3 <= CONFIG["minimum_mesh_levels"] <= len(sizes):
        raise ValueError("Minimum mesh levels must be between three and the scheduled mesh count")
    if not 1 <= CONFIG["required_successive_comparisons"] < len(sizes):
        raise ValueError("Invalid number of required successive comparisons")


def begin_gmsh():
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("General.NumThreads", 2)


def extract_lid():
    source = (HERE / CONFIG["source_step"]).resolve()
    begin_gmsh()
    try:
        gmsh.model.occ.importShapes(str(source))
        gmsh.model.occ.synchronize()
        matches = [item for item in gmsh.model.getEntities(3)
                   if CONFIG["body_name_contains"] in gmsh.model.getEntityName(*item)]
        if len(matches) != 1:
            raise ValueError(f"Expected one named lid solid, found {matches}")
        lid = matches[0]
        name = gmsh.model.getEntityName(*lid)
        original_bounds = gmsh.model.getBoundingBox(*lid)
        volume = gmsh.model.occ.getMass(*lid)
        others = [item for item in gmsh.model.getEntities(3) if item != lid]
        gmsh.model.occ.remove(others, recursive=True)
        z_shift = -round(original_bounds[2], 6)
        gmsh.model.occ.translate([lid], 0, 0, z_shift)
        gmsh.model.occ.synchronize()
        if len(gmsh.model.getEntities(3)) != 1:
            raise ValueError("Geometry isolation did not leave exactly one lid solid")
        bounds = [round(x, 6) for x in gmsh.model.getBoundingBox(*lid)]
        faces = gmsh.model.getBoundary([lid], oriented=False)
        holes = []
        for dim, tag in faces:
            if gmsh.model.getType(dim, tag) == "Cylinder":
                box = gmsh.model.getBoundingBox(dim, tag)
                holes.append({"center_mm": list(gmsh.model.occ.getCenterOfMass(dim, tag)),
                              "radius_mm": round((box[3] - box[0]) / 2, 6)})
        if len(holes) != 4:
            raise ValueError(f"Expected four cylindrical mounting holes, found {len(holes)}")
        gmsh.write(str(OUT / "lid.step"))
        return {"source_step_sha256": digest(source), "source_body_name": name,
                "original_bounds_mm": list(original_bounds), "z_translation_mm": z_shift,
                "analysis_bounds_mm": bounds,
                "dimensions_mm": [bounds[i + 3] - bounds[i] for i in range(3)],
                "cad_volume_mm3": volume, "screw_holes": holes}
    finally:
        gmsh.finalize()


def generate_mesh(size, label):
    begin_gmsh()
    gmsh.logger.start()
    try:
        gmsh.model.occ.importShapes(str(OUT / "lid.step"))
        gmsh.model.occ.synchronize()
        body = gmsh.model.getEntities(3)[0]
        bounds = gmsh.model.getBoundingBox(*body)
        ztop = bounds[5]
        top, supports = [], []
        for dim, tag in gmsh.model.getBoundary([body], oriented=False):
            box = gmsh.model.getBoundingBox(dim, tag)
            kind = gmsh.model.getType(dim, tag)
            if abs(box[2] - ztop) < 1e-5 and abs(box[5] - ztop) < 1e-5:
                top.append(tag)
            if kind == "Cylinder":
                supports.append(tag)
        if len(top) != 1 or len(supports) != 4:
            raise ValueError(f"Unexpected boundary selection: top={top}, supports={supports}")
        for dim, entities, tag, name in [(2, top, 1, "loaded_top"),
                                         (2, supports, 2, "screw_walls"),
                                         (3, [body[1]], 3, "lid")]:
            gmsh.model.addPhysicalGroup(dim, entities, tag)
            gmsh.model.setPhysicalName(dim, tag, name)
        gmsh.option.setNumber("Mesh.MeshSizeMax", size)
        gmsh.option.setNumber("Mesh.MeshSizeMin", min(0.65, size))
        gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 12)
        gmsh.model.mesh.setSize(gmsh.model.getEntities(0), size)
        gmsh.option.setNumber("Mesh.Algorithm3D", 1)
        gmsh.option.setNumber("Mesh.ElementOrder", 1)
        gmsh.option.setNumber("Mesh.MshFileVersion", 4.1)
        gmsh.option.setNumber("Mesh.Binary", 1)
        gmsh.option.setNumber("Mesh.RandomSeed", 7)
        gmsh.model.mesh.generate(3)
        gmsh.model.mesh.optimize("Netgen")
        element_tags, _ = gmsh.model.mesh.getElementsByType(4)
        quality = np.asarray(gmsh.model.mesh.getElementQualities(element_tags, "minSICN"))
        if not len(quality) or np.min(quality) <= 0:
            raise ValueError("Empty or invalid tetrahedral mesh")
        mesh_path = MESHES / f"{label}.msh"
        gmsh.write(str(mesh_path))
        (OUT / f"{label}_mesher.log").write_text("\n".join(gmsh.logger.get()) + "\n")
        return mesh_path, {"quality_min_SICN": float(quality.min()),
                           "quality_p05_SICN": float(np.quantile(quality, .05)),
                           "quality_mean_SICN": float(quality.mean())}
    finally:
        gmsh.logger.stop()
        gmsh.finalize()


def stress_from_gradient(gradient, lam, mu):
    strain = .5 * (gradient + np.swapaxes(gradient, 0, 1))
    trace = np.einsum("ii...->...", strain)
    eye = np.eye(3).reshape((3, 3) + (1,) * trace.ndim)
    return 2 * mu * strain + lam * eye * trace


def von_mises(stress):
    return np.sqrt(.5 * ((stress[0, 0] - stress[1, 1])**2
                        + (stress[1, 1] - stress[2, 2])**2
                        + (stress[2, 2] - stress[0, 0])**2)
                   + 3 * (stress[0, 1]**2 + stress[1, 2]**2 + stress[2, 0]**2))


def stress_at_points(basis, displacement, points, lam, mu):
    """Evaluate the unsmoothed FE gradient at fixed physical coordinates."""
    cells = basis.mesh.element_finder(mapping=basis.mapping)(*points)
    reference = basis.mapping.invF(points[:, :, None], tind=cells)
    gradient = np.zeros((3, 3, points.shape[1], 1))
    for k in range(basis.Nbfun):
        field = basis.elem.gbasis(basis.mapping, reference, k, tind=cells)[0]
        gradient += field.grad * displacement[basis.element_dofs[k, cells]][None, None, :, None]
    return stress_from_gradient(gradient, lam, mu)[:, :, :, 0]


def verify_solver():
    """Independent analytical uniaxial-tension patch test and probe check."""
    mesh = MeshTet().refined(2)
    basis = Basis(mesh, ELEMENT, intorder=4)
    e, nu, traction = 2000., .35, 1.
    lam, mu = lame_parameters(e, nu)
    right = mesh.facets_satisfying(lambda x: np.isclose(x[0], 1))
    @LinearForm
    def tension(v, w):
        return traction * v[0]
    force = asm(tension, basis.boundary(right))
    constrained = np.unique(np.concatenate([
        basis.get_dofs(lambda x: np.isclose(x[0], 0)).all(["u^1"]),
        basis.get_dofs(lambda x: np.isclose(x[1], 0)).all(["u^2"]),
        basis.get_dofs(lambda x: np.isclose(x[2], 0)).all(["u^3"])]))
    matrix = asm(linear_elasticity(lam, mu), basis)
    u = solve(*condense(matrix, force, D=constrained))
    expected = np.zeros(basis.N)
    for component, indexes in enumerate(basis.split_indices()):
        expected[indexes] = basis.doflocs[component, indexes] * traction / e * (1 if component == 0 else -nu)
    relative_displacement_error = float(np.linalg.norm(u - expected) / np.linalg.norm(expected))
    points = np.array([[.23, .61], [.31, .41], [.37, .73]])
    stress = stress_at_points(basis, u, points, lam, mu)
    expected_stress = np.zeros_like(stress)
    expected_stress[0, 0] = traction
    stress_error = float(np.max(np.abs(stress - expected_stress)))
    if relative_displacement_error > 1e-8 or stress_error > 1e-7:
        raise AssertionError("Analytical elasticity patch test failed")
    result = {"test": "Unit-cube uniaxial traction with analytical Poisson contraction",
              "relative_displacement_error": relative_displacement_error,
              "maximum_stress_component_error_mpa": stress_error,
              "passed": True}
    save_json(OUT / "solver_verification.json", result)
    print("Analytical solver/probe verification: PASS", flush=True)


def figure_save(fig, stem):
    fig.savefig(PLOTS / f"{stem}.png", dpi=180, bbox_inches="tight")
    fig.savefig(PLOTS / f"{stem}.svg", bbox_inches="tight")
    plt.close(fig)


def top_faces(mesh, ztop):
    return mesh.facets_satisfying(lambda x: np.isclose(x[2], ztop, atol=1e-6))


def mesh_plot(mesh, top, label, row):
    triangles = mesh.facets[:, top].T
    edges = np.vstack([triangles[:, [0, 1]], triangles[:, [1, 2]], triangles[:, [2, 0]]])
    lines = mesh.p[:2, edges].transpose(1, 2, 0)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.add_collection(LineCollection(lines, colors=COLORS["teal"], linewidths=.32))
    ax.autoscale()
    ax.set_aspect("equal")
    ax.set(xlabel="x (mm)", ylabel="y (mm)",
           title=f"{label}: top-surface mesh of actual lid")
    ax.text(.01, -.16, f"{row['tetrahedra']:,} tetrahedra | {row['geometric_vertices']:,} geometric vertices | "
            f"{row['p2_nodes']:,} quadratic displacement nodes\nMinimum SICN: {row['quality_min_SICN']:.3f} | "
            "Straight-sided geometric cells; quadratic displacement field", transform=ax.transAxes)
    figure_save(fig, f"mesh_{label}")


def solve_level(mesh_path, quality, size, label, geometry):
    start = time.perf_counter()
    mesh = MeshTet.load(str(mesh_path))
    basis = Basis(mesh, ELEMENT, intorder=4)
    if basis.N > CONFIG["maximum_displacement_dofs"]:
        raise RuntimeError(f"DOF limit exceeded ({basis.N}); refine on a machine with more RAM")
    lam, mu = lame_parameters(CONFIG["youngs_modulus_mpa"], CONFIG["poisson_ratio"])
    top_basis = basis.boundary("loaded_top")
    area = float(top_basis.dx.sum())
    pressure = CONFIG["total_downward_force_n"] / area
    @LinearForm
    def downward(v, w):
        return -pressure * v[2]
    force = asm(downward, top_basis)
    constrained = basis.get_dofs("screw_walls").all()
    print(f"{label}: assembling {mesh.nelements:,} tets / {basis.N:,} DOFs", flush=True)
    matrix = asm(linear_elasticity(lam, mu), basis)
    u = solve(*condense(matrix, force, D=constrained))
    residual = matrix @ u - force
    component_indices = basis.split_indices()
    applied = np.array([force[i].sum() for i in component_indices])
    reactions = np.array([residual[np.intersect1d(i, constrained)].sum() for i in component_indices])
    equilibrium_error = float(np.linalg.norm(applied + reactions) / CONFIG["total_downward_force_n"])
    free = np.setdiff1d(np.arange(basis.N), constrained)
    free_residual = float(np.linalg.norm(residual[free]) / np.linalg.norm(force))
    if equilibrium_error > 1e-6 or free_residual > 1e-6 or not np.isfinite(u).all():
        raise AssertionError("Force balance or linear solve residual failed")
    bounds = geometry["analysis_bounds_mm"]
    center = np.array([(bounds[0] + bounds[3]) / 2, (bounds[1] + bounds[4]) / 2,
                       (bounds[2] + bounds[5]) / 2])
    thickness = bounds[5] - bounds[2]
    probe_z = bounds[5] - CONFIG["stress_probe_depth_fraction"] * thickness
    offsets = CONFIG["stress_probe_offsets_mm"]
    points = np.array([[center[0] + dx, center[1] + dy, probe_z]
                       for dx in offsets for dy in offsets]).T
    probe_stress = stress_at_points(basis, u, points, lam, mu)
    probe_vm = von_mises(probe_stress)
    center_u = basis.interpolator(u)(center[:, None])[:, 0]
    gradient = basis.interpolate(u).grad
    stress = stress_from_gradient(gradient, lam, mu)
    vm = von_mises(stress)
    vm_cell = (vm * basis.dx).sum(axis=1) / basis.dx.sum(axis=1)
    nodal_u = u[basis.nodal_dofs].T
    vector_dofs = np.vstack([u[i] for i in component_indices])
    row = {"level": label, "target_mesh_size_mm": size,
           "tetrahedra": int(mesh.nelements), "geometric_vertices": int(mesh.nvertices),
           "p2_nodes": int(basis.N // 3), "displacement_dofs": int(basis.N),
           "constrained_dofs": int(len(constrained)), "loaded_area_mm2": area,
           "pressure_mpa": pressure, "applied_force_z_n": float(applied[2]),
           "support_reaction_z_n": float(reactions[2]),
           "force_balance_relative_error": equilibrium_error,
           "free_dof_relative_residual": free_residual,
           "center_uz_mm": float(center_u[2]),
           "max_displacement_at_p2_nodes_mm": float(np.linalg.norm(vector_dofs, axis=0).max()),
           "central_patch_mean_vm_mpa": float(probe_vm.mean()),
           "central_patch_min_vm_mpa": float(probe_vm.min()),
           "central_patch_max_vm_mpa": float(probe_vm.max()),
           "global_quadrature_max_vm_mpa": float(vm.max()),
           "strain_energy_n_mm": float(.5 * u @ (matrix @ u)),
           "solve_and_postprocess_seconds": time.perf_counter() - start, **quality}
    if row["max_displacement_at_p2_nodes_mm"] / thickness >= .1:
        raise AssertionError("Displacement is too large for the selected preliminary small-displacement model")
    meshio.write(OUT / f"{label}.vtu", meshio.Mesh(mesh.p.T, [("tetra", mesh.t.T)],
                  point_data={"displacement_mm": nodal_u},
                  cell_data={"cell_mean_von_mises_mpa": [vm_cell]}))
    np.savez_compressed(OUT / f"{label}_solution.npz", displacement_dofs=u,
                        probe_points_mm=points, probe_von_mises_mpa=probe_vm,
                        fixed_dofs=constrained, element_quality_metric=np.array([quality["quality_min_SICN"]]))
    top = top_faces(mesh, bounds[5])
    mesh_plot(mesh, top, label, row)
    save_json(OUT / f"{label}_statistics.json", row)
    np.savez_compressed(OUT / f"{label}_surface.npz", points=mesh.p,
                        triangles=mesh.facets[:, top].T, displacement=nodal_u,
                        von_mises_top_cell_mpa=vm_cell[mesh.f2t[0, top]])
    print(f"{label}: uz={center_u[2]:.7f} mm, probe VM={probe_vm.mean():.6f} MPa, "
          f"balance={equilibrium_error:.2e}", flush=True)
    del basis, matrix, gradient, stress, vm, u, mesh
    gc.collect()
    return row


def change(new, old):
    return 100 * abs(new - old) / max(abs(new), 1e-15)


def write_table(rows):
    with (OUT / "mesh_statistics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[-1]))
        writer.writeheader()
        writer.writerows(rows)


def plots(rows, geometry):
    count = [row["tetrahedra"] for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    series = [("center_uz_mm", "Center deflection magnitude (mm)", COLORS["teal"]),
              ("central_patch_mean_vm_mpa", "Fixed central-patch mean von Mises (MPa)", COLORS["amber"])]
    for ax, (key, ylabel, color) in zip(axes, series):
        values = [abs(row[key]) for row in rows]
        ax.plot(count, values, "o-", color=color, linewidth=2)
        for x, y, row in zip(count, values, rows):
            ax.annotate(f"h={row['target_mesh_size_mm']:g}", (x, y), xytext=(4, 6), textcoords="offset points", fontsize=8)
        ax.set(xlabel="Number of tetrahedral elements", ylabel=ylabel)
        ax.grid(alpha=.2)
    fig.suptitle("Actual mesh-refinement results | assumed material and loading", color=COLORS["navy"])
    fig.tight_layout()
    figure_save(fig, "convergence")
    last = rows[-1]
    surface = np.load(OUT / f"{last['level']}_surface.npz")
    p, triangles = surface["points"], surface["triangles"]
    tri = mtri.Triangulation(p[0], p[1], triangles)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.3))
    image = axes[0].tripcolor(tri, -surface["displacement"][:, 2], shading="gouraud", cmap="viridis")
    fig.colorbar(image, ax=axes[0], label="Downward displacement (mm)", shrink=.75)
    axes[0].set_title("Top-face displacement: vertex samples")
    image = axes[1].tripcolor(tri, facecolors=surface["von_mises_top_cell_mpa"], shading="flat", cmap="magma")
    fig.colorbar(image, ax=axes[1], label="Cell-average von Mises (MPa)", shrink=.75)
    axes[1].set_title("Top-adjacent cells: unsmoothed stress")
    for ax in axes:
        ax.set_aspect("equal")
        ax.set(xlabel="x (mm)", ylabel="y (mm)")
    fig.suptitle("Preliminary linear-static lid response | no strength pass/fail", color=COLORS["navy"])
    fig.tight_layout()
    figure_save(fig, "response")
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d", proj_type="ortho", computed_zorder=False)
    ax.add_collection3d(Poly3DCollection(p[:, triangles].transpose(1, 2, 0),
                        facecolor="#eef4f5", edgecolor="#98aab4", linewidth=.15, zorder=1))
    bounds = geometry["analysis_bounds_mm"]
    xmin, ymin, zmin, xmax, ymax, zmax = bounds
    cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
    for hole in geometry["screw_holes"]:
        x, y, _ = hole["center_mm"]
        angle = np.linspace(0, 2 * np.pi, 50)
        for z in (zmin, zmax):
            ax.plot(x + hole["radius_mm"] * np.cos(angle), y + hole["radius_mm"] * np.sin(angle),
                    np.full_like(angle, z), color=COLORS["teal"], linewidth=2)
        ax.plot([x, x], [y, y], [zmin, zmax], color=COLORS["teal"], linewidth=2)
    arrow_height = max((xmax - xmin) * .13, zmax - zmin)
    for x in np.linspace(xmin + .15 * (xmax - xmin), xmax - .15 * (xmax - xmin), 5):
        for y in np.linspace(ymin + .2 * (ymax - ymin), ymax - .2 * (ymax - ymin), 3):
            ax.quiver(x, y, zmax + arrow_height, 0, 0, -arrow_height,
                      color=COLORS["red"], arrow_length_ratio=.15, linewidth=1.4, zorder=5)
    offsets = CONFIG["stress_probe_offsets_mm"]
    ax.scatter([cx + dx for dx in offsets for _ in offsets],
               [cy + dy for _ in offsets for dy in offsets],
               [zmax] * len(offsets)**2, marker="x", color=COLORS["amber"], depthshade=False)
    ax.set(xlabel="x (mm)", ylabel="y (mm)", zlabel="z (mm)",
           title="Actual lid geometry and assumed loading/supports",
           xlim=(xmin - 4, xmax + 4), ylim=(ymin - 4, ymax + 4),
           zlim=(zmin, zmax + 1.2 * arrow_height))
    ax.set_box_aspect((xmax - xmin + 8, ymax - ymin + 8, zmax - zmin + 1.2 * arrow_height))
    ax.set_zticks([zmin, zmax, zmax + .5 * arrow_height, zmax + arrow_height])
    ax.view_init(elev=34, azim=-55)
    fig.text(.08, .06, "Teal: fixed screw-hole walls. Red: uniform downward (-z) traction; arrow length is schematic.\n"
             f"Total force = {CONFIG['total_downward_force_n']:g} N; E = {CONFIG['youngs_modulus_mpa']:g} MPa; "
             f"nu = {CONFIG['poisson_ratio']:g}, all assumed.\n"
             "Amber marks the plan locations of fixed stress probes inside the upper portion of the lid.")
    figure_save(fig, "setup")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--plots-only", action="store_true")
    args = parser.parse_args()
    validate_configuration()
    for folder in (OUT, MESHES, PLOTS):
        folder.mkdir(parents=True, exist_ok=True)
    if args.plots_only:
        summary = json.loads((OUT / "summary.json").read_text())
        plots(summary["levels"], summary["geometry"])
        from build_report import build_report
        build_report()
        return
    verify_solver()
    if args.verify_only:
        return
    geometry = extract_lid()
    save_json(OUT / "geometry.json", geometry)
    rows, consecutive = [], 0
    tolerance = CONFIG["comparison_tolerance_percent"]
    for index, size in enumerate(CONFIG["mesh_sizes_mm"], 1):
        label = f"mesh_{index:02d}"
        mesh_path, quality = generate_mesh(size, label)
        row = solve_level(mesh_path, quality, size, label, geometry)
        row["deflection_change_percent"] = None
        row["probe_stress_change_percent"] = None
        if rows:
            row["deflection_change_percent"] = change(row["center_uz_mm"], rows[-1]["center_uz_mm"])
            row["probe_stress_change_percent"] = change(row["central_patch_mean_vm_mpa"], rows[-1]["central_patch_mean_vm_mpa"])
            success = max(row["deflection_change_percent"], row["probe_stress_change_percent"]) < tolerance
            consecutive = consecutive + 1 if success else 0
        rows.append(row)
        write_table(rows)
        summary = {"configuration": CONFIG, "geometry": geometry, "levels": rows,
                   "successive_mesh_criterion_met": consecutive >= CONFIG["required_successive_comparisons"] and len(rows) >= CONFIG["minimum_mesh_levels"],
                   "consecutive_comparisons_below_tolerance": consecutive,
                   "software": {name: importlib.metadata.version(name) for name in
                                ["gmsh", "scikit-fem", "numpy", "scipy", "matplotlib", "meshio"]},
                   "python": platform.python_version(), "platform": platform.platform()}
        save_json(OUT / "summary.json", summary)
        if len(rows) >= CONFIG["minimum_mesh_levels"] and summary["successive_mesh_criterion_met"]:
            break
    plots(rows, geometry)
    from build_report import build_report
    build_report()
    print("Study complete. Successive-mesh criterion met: " + str(summary["successive_mesh_criterion_met"]), flush=True)


if __name__ == "__main__":
    main()
