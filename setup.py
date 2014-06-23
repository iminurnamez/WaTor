import sys
from cx_Freeze import setup, Executable

base = None 
if sys.platform == "win32":
    base = "Win32GUI"
   
exe = Executable(script="wator.py", base=base)
 
include_files=["resources/music", "resources/graphics", "resources/sound",
                     "resources/fonts"]
includes=[]
excludes=["Tkinter"]
packages=[]

setup(version="1.0",
         description="Wa-Tor Population Dynamics Simulation",
         author="Erf",
         name="Wa-Tor",
         options={"build_exe": {"includes": includes, "include_files": include_files, "packages": packages, "excludes": excludes}},
         executables=[exe])

