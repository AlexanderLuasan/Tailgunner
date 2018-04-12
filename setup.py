import sys
import cx_Freeze 



build_exe_options = {"packages": ["os","pygame","codecs"], "excludes": ["tkinter"],"include_files" : ["zeroTurn.png","ThunderboltTurns.png","water.png"]}


cx_Freeze.setup(  name = "TailGunner",
        version = "0.1",
        description = "GameProject",
        options = {"build_exe": build_exe_options},
        executables = [cx_Freeze.Executable("main.py")])


