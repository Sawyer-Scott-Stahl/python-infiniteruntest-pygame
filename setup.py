import cx_Freeze
import os

executables = [cx_Freeze.Executable("game.py", base="Win32GUI")]

os.environ['TCL_LIBRARY'] = r"C:\Users\Sawyer\AppData\Local\Programs\Python\Python37\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\Sawyer\AppData\Local\Programs\Python\Python37\tcl\tk8.6"

cx_Freeze.setup(
    name="Infinite Run Test",
    options={"build_exe": {"packages": ["pygame", "sys", "random"],
                           "include_files": ["Chunkfive.otf", "opensans.ttf"]}},
    executables=executables
    )
