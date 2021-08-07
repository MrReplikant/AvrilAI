:: Windows installer

@echo off

:: update embeddable package from https://www.python.org/downloads/windows/
set PythonURL=https://www.python.org/ftp/python/3.9.5/python-3.9.5-embed-amd64.zip
set PythonPathFile=python39._pth

:: update from https://github.com/microsoft/terminal/releases
set WindowsTerminalURL=https://github.com/microsoft/terminal/releases/download/v1.7.1091.0/Microsoft.WindowsTerminal_1.7.1091.0_8wekyb3d8bbwe.msixbundle

:: Checking if the user has curl and tar installed
for %%X in (curl.exe) do (set HasCurl=%%~$PATH:X)
for %%X in (tar.exe) do (set HasTar=%%~$PATH:X)


echo AIDungeon2 Clover Edition installer for Windows 10 64-bit
echo ----------------------------------------------------------------------------------------------
echo.
echo Please disable your anti-virus before continuing the install process.
echo.
echo.
echo Using an Nvidia GPU requires 6 GB HDD space, 16 GB RAM, and at least 6 GB of VRAM on your GPU for GPT-2 or up to 8 GB of VRAM for GPT-Neo.
echo Using only your CPU requires 2 GB HDD space, 16 GB RAM.
echo Additionally, models require between 6 and 10 GB HDD space each, and you will need at least one.
echo.
:: console bell
echo 
:selectcuda
echo 1) Install Nvidia GPU (CUDA) version
echo 2) Install CPU-only version
echo 0) Cancel
set /p usecuda="Enter your choice: "
if %usecuda%==1 (goto install)
if %usecuda%==2 (goto install)
if %usecuda%==0 (exit) else (goto selectcuda)

:install
echo.

:: Create /venv/
echo Creating ./venv/
if not exist "./venv" mkdir venv

cd venv

:: Download Python
echo Downloading Python...
if defined HasCurl (
  curl "%PythonURL%" -o "%cd%\python.zip"
) else (
  powershell Invoke-WebRequest -Uri "%PythonURL%" -OutFile "%cd%\python.zip"
)


:: Extract Python
echo Extracting Python
if defined HasTar (
  tar -xf "python.zip"
) else (
  powershell Expand-Archive python.zip ./ -Force
)

:: Get pip
echo Downloading pip...
if defined HasCurl (
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
) else (
  powershell Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "%cd%\get-pip.py"
)
echo Installing pip
python.exe get-pip.py --no-warn-script-location
echo Lib\site-packages>>%PythonPathFile%
echo ..>>%PythonPathFile%

:: For lazy use down below
SET PY="%CD%\python.exe"

:: Delete zip
echo Removing temporary files
del python.zip
del get-pip.py

cd ..

:: Install Requirements
echo Installing universal dependencies
%PY% -m pip --no-cache-dir install -r requirements/requirements.txt --no-color --no-warn-script-location

:: Install Torch
echo Installing PyTorch
if %usecuda%==1 (
  %PY% -m pip install -r requirements/cuda_requirements.txt --no-color --no-warn-script-location
)
if %usecuda%==2 (
  %PY% -m pip install -r requirements/cpu_requirements.txt --no-color --no-warn-script-location
)

:: Check for and offer to help install Windows Terminal
for %%X in (wt.exe) do (set HasWT=%%~$PATH:X)
if defined HasWT (goto models)
echo.
echo Microsoft Windows Terminal was not found.
echo It is highly recommended you install it.
:: console bell
echo 
:selectwt
set /p openwt="Would you like to install Microsoft Windows Terminal now? (y/n) "
if "%openwt%"=="y" (
  if defined HasCurl (
    curl -L "%WindowsTerminalURL%" -o wt.msixbundle
  ) else (
    powershell Invoke-WebRequest -Uri "%WindowsTerminalURL%" -OutFile "%cd%\wt.msixbundle"
  )
  start "" /wait /b wt.msixbundle
  pause
  del wt.msixbundle
  goto models
)
if "%openwt%"=="n" (goto models) else (goto selectwt)

:models

echo.
echo You now need to download a model. See README.md for more details and links.
echo When you have a model, just double-click play.bat to play!
:: console bell
echo 
pause
