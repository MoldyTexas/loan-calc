import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    
# Define the setup
setup(
    name="Loan Calculator",
    version="1.0",
    description="A simple loan calculator application",
    executables=[Executable("calculator.py")]
)
