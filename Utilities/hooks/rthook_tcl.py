"""
Runtime hook — runs at EXE startup before any Python imports.
Sets TCL_LIBRARY and TK_LIBRARY to the directories bundled inside the EXE
so that tkinter finds the correct init.tcl that matches the bundled DLL version.
"""

import os
import sys

if getattr(sys, "frozen", False):
    base = sys._MEIPASS
    tcl_path = os.path.join(base, "_tcl_data")
    tk_path = os.path.join(base, "_tk_data")
    if os.path.isdir(tcl_path):
        os.environ["TCL_LIBRARY"] = tcl_path
    if os.path.isdir(tk_path):
        os.environ["TK_LIBRARY"] = tk_path
