from cx_Freeze import setup,Executable
setup(
    name="GABEN",
    version=1.1,
    description="GABEN_NEWS",
    executables=[Executable("main.py")],
)
    # executables=[Executable("main.py",base="Win32GUI")],
