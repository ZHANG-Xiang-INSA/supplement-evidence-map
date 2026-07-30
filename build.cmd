@echo off
REM Rebuild index.html, both markdown companions and README.md from src/.
REM Output lands in this folder. No dependencies beyond the Python standard library.
setlocal
cd /d "%~dp0src" || exit /b 1
set PYTHONIOENCODING=utf-8

echo Building page...
py -3 assemble.py || exit /b 1
echo Building markdown...
py -3 md.py       || exit /b 1
echo Building README...
py -3 readme.py   || exit /b 1

echo.
echo Done. Open index.html to view.
endlocal
