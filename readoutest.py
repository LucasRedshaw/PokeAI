import subprocess
import os

# Command to open a new PowerShell window and run a script
cmd1 = 'start powershell -NoExit -Command "python -c \\"print(\'Hello from first window!\')\\""'
cmd2 = 'start powershell -NoExit -Command "python -c \\"print(\'Hello from second window!\')\\""'

# Open the first terminal window
subprocess.Popen(cmd1, shell=True)

# Open the second terminal window
subprocess.Popen(cmd2, shell=True)
