"""
patch_tcl_init.py

Post-build script called by build_exe.bat.

PyInstaller bundles its own init.tcl that may contain:
    package require -exact Tcl 8.6.12
but Anaconda ships tcl86t.dll at version 8.6.10, causing a runtime crash.

This script finds init.tcl files inside the dist directory and replaces them
with the one from the active Python's Tcl installation so the version strings
always match the bundled DLL.

Usage:
    python patch_tcl_init.py <dist_app_dir>
"""

import glob
import os
import shutil
import sys


def find_source_init_tcl() -> str | None:
    """Return the path to init.tcl from the active Python's Tcl installation."""
    search_roots = [
        os.path.join(sys.prefix, "tcl"),
        os.path.join(sys.prefix, "Library", "lib"),
        os.path.join(sys.prefix, "lib"),
    ]
    for root in search_roots:
        if not os.path.isdir(root):
            continue
        for entry in sorted(os.listdir(root)):
            if entry.lower().startswith("tcl") and os.path.isdir(os.path.join(root, entry)):
                candidate = os.path.join(root, entry, "init.tcl")
                if os.path.isfile(candidate):
                    return candidate
    return None


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python patch_tcl_init.py <dist_app_dir>")
        return 1

    dist_dir = sys.argv[1]
    if not os.path.isdir(dist_dir):
        print(f"ERROR: dist directory not found: {dist_dir}")
        return 1

    src = find_source_init_tcl()
    if not src:
        print("ERROR: Could not locate init.tcl in the active Python installation.")
        print(f"  Searched under: {sys.prefix}")
        return 1

    print(f"Source init.tcl : {src}")

    targets = glob.glob(os.path.join(dist_dir, "**", "init.tcl"), recursive=True)
    if not targets:
        print(f"WARNING: No init.tcl found under {dist_dir} — nothing to patch.")
        return 0

    for target in targets:
        shutil.copy2(src, target)
        print(f"Patched         : {target}")

    print("Tcl init.tcl patch complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
