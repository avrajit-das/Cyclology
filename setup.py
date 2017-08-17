"""setup script for creating windows executable with cx_freeze"""
import sys
from cx_Freeze import setup, Executable
import os

# Set missing path variables
python_path = r"C:\Users\EUC\AppData\Local\Programs\Python\Python35"
os.environ['TCL_LIBRARY'] = os.path.join(python_path, "tcl", "tcl8.6")
os.environ['TK_LIBRARY'] = os.path.join(python_path, "tcl", "tk8.6")

package_list = ["FreeMark", "tkinter", "os", "PIL", "threading", "queue", "re"]

# Required files in include folder:
# tk86t.dll
# tcl86t.dll
# From the tcl subfolder of the python folder
build_exe_options = {"packages": package_list,
                     "include_files": [os.path.join("include", file) for file
                                       in os.listdir("include")]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable("FreeMark.py",
                 base=base,
                 targetName="FreeMark.exe",
                 icon='logo.ico')

setup(name="FreeMark",
      version="0.0.3",
      description="Watermark images, easily",
      options={"build_exe": build_exe_options},
      executables=[exe])
