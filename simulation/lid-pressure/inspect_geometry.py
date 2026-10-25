"""Inspect the real STEP assembly before choosing an analysis body."""
from pathlib import Path
import json
import gmsh

ROOT = Path(__file__).resolve().parents[2]
gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)
gmsh.model.occ.importShapes(str(ROOT / "cad" / "VKA2026.step"))
gmsh.model.occ.synchronize()
bodies = []
for dim, tag in gmsh.model.getEntities(3):
    bounds = gmsh.model.getBoundingBox(dim, tag)
    bodies.append({
        "tag": tag,
        "name": gmsh.model.getEntityName(dim, tag),
        "bounds_mm": list(bounds),
        "size_mm": [round(bounds[i + 3] - bounds[i], 6) for i in range(3)],
        "volume_mm3": gmsh.model.occ.getMass(dim, tag),
    })
print(json.dumps(sorted(bodies, key=lambda b: b["volume_mm3"], reverse=True)[:12], indent=2))
gmsh.finalize()
