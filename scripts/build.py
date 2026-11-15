#!/usr/bin/env python3
"""Build and inspect a deterministic, single-plugin ZIP outside its source."""
import hashlib
import json
from pathlib import Path
import stat
import zipfile

from validate import ROOT, read_json, require, scan_bytes, validate


def build(root=ROOT):
    validate(root)
    package = root / "plugins/tactical-rmm"
    manifest = read_json(package / "plugin.json")
    files = sorted(p for p in package.rglob("*") if p.is_file())
    out = root / "dist"
    out.mkdir(exist_ok=True)
    archive = out / f"tactical-rmm-{manifest['version']}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in files:
            info = zipfile.ZipInfo("tactical-rmm/" + path.relative_to(package).as_posix(), (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            z.writestr(info, path.read_bytes())
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, "Corrupt archive")
        names = set(z.namelist())
        require(names == {"tactical-rmm/" + p.relative_to(package).as_posix() for p in files}, "Archive/source mismatch")
        require("tactical-rmm/.app.json" in names, "Hidden app reference missing")
        require(not any("marketplace" in n or ".." in Path(n).parts for n in names), "Invalid archive contents")
        for name in names:
            data = z.read(name)
            scan_bytes(data, name)
            if name.endswith(".json"):
                json.loads(data)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.sha256").write_text(f"{digest}  {archive.name}\n")
    print(json.dumps({"archive": str(archive), "files": len(files), "sha256": digest}))
    return archive


if __name__ == "__main__":
    build()
