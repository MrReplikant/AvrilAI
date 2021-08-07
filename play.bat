@echo off
set PY="%CD%\venv\python.exe"

for %%X in (wt.exe) do (set FOUNDWT=%%~$PATH:X)
if not defined FOUNDWT (
    start "AIDungeon2 Clover Edition" %PY% launch.py
) else (
    wt.exe --title "AIDungeon2 Clover Edition" -d "%~dp0/" -p "Windows PowerShell" %PY% launch.py
)
