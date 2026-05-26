@echo off
setlocal enabledelayedexpansion
REM 1_extrair.bat - extrai SYSTEM.MSG e SI_*.DAT da ISO

cd /d "%~dp0"
echo === ILHM EXTRACT ===
echo Pasta atual: %CD%
echo.

set "ISO=Innocent Life - A Futuristic Harvest Moon - Special Edition (USA).iso"

if not exist "!ISO!" goto :iso_missing

echo Verificando Python...
where python >nul 2>&1
if errorlevel 1 goto :no_python

echo Verificando pycdlib...
python -c "import pycdlib" 2>nul
if errorlevel 1 (
    echo pycdlib nao instalado. Instalando...
    python -m pip install pycdlib
    if errorlevel 1 goto :pip_failed
)

echo.
echo === Extraindo arquivos da ISO ===
python "tools\ilhm_extract.py" --iso "!ISO!" --work "work"
if errorlevel 1 goto :extract_failed

echo.
echo Pronto. Edita arquivos em work\translated\ depois roda 2_aplicar.bat.
pause
exit /b 0

:iso_missing
echo ERRO: ISO original nao encontrada em:
echo   %CD%\!ISO!
pause
exit /b 1

:no_python
echo ERRO: 'python' nao encontrado no PATH.
echo Instale Python e marca "Add Python to PATH": https://www.python.org/downloads/
pause
exit /b 1

:pip_failed
echo Falha ao instalar pycdlib.
pause
exit /b 1

:extract_failed
echo Extracao falhou.
pause
exit /b 1
