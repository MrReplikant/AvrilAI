@echo off
:Installer provided by the KoboldAI Project
title AvrilAI Runtime Installer (MicroMamba)
echo Errors? Rerun this as admin so it can add the needed LongPathsEnabled registery tweak.
echo Installer failed or crashed? Run it again so it can continue.
echo Only Windows 10 and higher officially supported, older Windows installations can't handle the paths.
echo.

Reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v "LongPathsEnabled" /t REG_DWORD /d "1" /f 2>nul
cd /D %~dp0

if exist miniconda3\ (
  echo Delete existing installation?
  echo This is required if you are switching modes, or if you get dependency errors in the game.
  echo 1. Yes
  echo 2. No
  SET /P D=Type the number of the desired option and then press ENTER: 
) ELSE (
	SET D=Workaround
)
IF %D%==1 rmdir /s /q miniconda3

:Mode
echo Which installation mode would you like?
echo 1. Temporary Drive Letter (Mounts the folder as drive A:, more stable and portable)
echo 2. Subfolder (Traditional method, can't run in folder paths that contain spaces)
echo.
SET /P M=Type the number of the desired option and then press ENTER: 
IF %M%==1 GOTO drivemap
IF %M%==2 GOTO subfolder
ECHO Incorrect choice
GOTO MODE


:drivemap
echo 1 > loader.settings
subst A: /D >nul
mkdir miniconda3 
subst A: miniconda3
SET TEMP=A:\
SET TMP=A:\
copy umamba.exe A:\umamba.exe
A:
umamba.exe create -r A:\python\ -n base
umamba.exe install --no-shortcuts -r A:\python\ -n base -f "%~dp0\environments\huggingface.yml" -y --always-copy
umamba.exe -r A:\ clean -a -y
rd A:\Python\pkgs /S /Q
subst A: /d
pause
exit

:subfolder
echo 2 > loader.settings
SET TEMP=%~DP0MINICONDA3
SET TMP=%~DP0MINICONDA3
umamba.exe create -r miniconda3\ -n base
umamba.exe install --no-shortcuts -r miniconda3 -n base -f environments\huggingface.yml -y --always-copy
umamba.exe clean -a -y
rd miniconda3\Python\pkgs /S /Q
pause
exit
