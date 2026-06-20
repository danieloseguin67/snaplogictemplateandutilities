"""
Custom hook for tkinter — overrides PyInstaller's built-in hook so that
Anaconda's Tcl/Tk libraries (not PyInstaller's cached copies) are bundled.

TCL_LIBRARY and TK_LIBRARY must be set in the environment before building.
"""

import os

from PyInstaller.utils.hooks import logger

tcl_lib = os.environ.get("TCL_LIBRARY", "")
tk_lib = os.environ.get("TK_LIBRARY", "")

hiddenimports = [
    "_tkinter",
    "tkinter",
    "tkinter.ttk",
    "tkinter.filedialog",
    "tkinter.messagebox",
]

datas = []

if tcl_lib and os.path.isdir(tcl_lib):
    datas.append((tcl_lib, "_tcl_data"))
    logger.info("hook-tkinter: Bundling TCL from %s", tcl_lib)
else:
    logger.warning(
        "hook-tkinter: TCL_LIBRARY not set or not found (%r); "
        "falling back to PyInstaller default — version mismatch may occur.",
        tcl_lib,
    )

if tk_lib and os.path.isdir(tk_lib):
    datas.append((tk_lib, "_tk_data"))
    logger.info("hook-tkinter: Bundling TK from %s", tk_lib)
else:
    logger.warning(
        "hook-tkinter: TK_LIBRARY not set or not found (%r); "
        "falling back to PyInstaller default.",
        tk_lib,
    )
