"""Package the real study and original source STEP with their relative paths."""
from pathlib import Path
import hashlib
import json
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TARGET = HERE.parent / "PranRakshak_Preliminary_Lid_FEA.zip"
files = sorted(p for p in HERE.rglob("*") if p.is_file()
               and "__pycache__" not in p.parts and p.suffix != ".pyc"
               and p.name != "manifest.json")
files.append(ROOT / "cad/VKA2026.step")
manifest = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size,
             "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
(HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
files.append(HERE / "manifest.json")
with zipfile.ZipFile(TARGET, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    archive.writestr("PranRakshak_FEA/OPEN_FIRST.txt",
                     "Open simulation/lid-pressure/Report.html for the visual report.\n"
                     "Read simulation/lid-pressure/README.md for assumptions and rerun instructions.\n"
                     "This is a preliminary assumed-material/load study, not a qualification test.\n"
                     "The original STEP and all meshes, results and scripts are included.\n")
    for path in files:
        archive.write(path, "PranRakshak_FEA/" + path.relative_to(ROOT).as_posix())
print(f"Packaged {len(files)} study/source files: {TARGET.name} ({TARGET.stat().st_size:,} bytes)")
