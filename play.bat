@echo off
cd /D %~dp0
TITLE AvrilAI
SET /P M=<loader.settings
IF %M%==1 GOTO drivemap
IF %M%==2 GOTO subfolder

:subfolder
ECHO Runtime launching in subfolder mode
SET TEMP=%~DP0MINICONDA3
SET TMP=%~DP0MINICONDA3
call miniconda3\condabin\activate
python launch.py %*
cmd /k

:drivemap
ECHO Runtime launching in A: drive mode
subst A: miniconda3 >nul
SET TEMP=A:\
SET TMP=A:\
call A:\python\condabin\activate
python launch.py %*
subst A: /D
cmd /k
