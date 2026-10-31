@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv-build\Scripts\python.exe" (
    py -3 -m venv ".venv-build"
    if errorlevel 1 goto :error
)

".venv-build\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt -r build-requirements.txt
if errorlevel 1 goto :error

".venv-build\Scripts\python.exe" create_icon.py
if errorlevel 1 goto :error

".venv-build\Scripts\python.exe" -m PyInstaller --noconfirm --clean --onefile --windowed --name "Kobra QR" --icon "%~dp0kobra_qr.ico" --distpath "dist" --workpath "build" --specpath "build" "main.py"
if errorlevel 1 goto :error

echo.
echo Application created: dist\Kobra QR.exe
pause
exit /b 0

:error
echo.
echo The build failed. Review the message above, then try again.
pause
exit /b 1
