@ECHO off
cd /d %~dp0 
call "./venv/Scripts/activate.bat"
echo "venv on"
cmd /k "dir && .\\venv\\Scripts\\python.exe main.py"
exit