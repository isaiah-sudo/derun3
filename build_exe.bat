@echo off
title CyberSurge 3D - Standalone EXE Builder
echo Building CyberSurge 3D into Standalone EXE...
python build_exe.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Build encountered an error.
    pause
    exit /b %ERRORLEVEL%
)
echo.
echo [*] Done! You can find the executable in dist\CyberSurge3D\CyberSurge3D.exe
pause
