@echo off
setlocal enabledelayedexpansion
REM 2_aplicar.bat - aplica traducoes na ISO PT (DAT + SCP)

cd /d "%~dp0"
echo === ILHM BUILD ===
echo Pasta atual: %CD%
echo.

set "ORIG=Innocent Life - A Futuristic Harvest Moon - Special Edition (USA).iso"
set "ISO_PT=InnocentLife_PT.iso"

if not exist "!ORIG!" goto :orig_missing

echo Verificando Python...
where python >nul 2>&1
if errorlevel 1 goto :no_python

echo Verificando dependencias (pycdlib, unicorn, capstone)...
python -c "import pycdlib, unicorn, capstone" 2>nul
if errorlevel 1 (
    echo Instalando dependencias faltantes...
    python -m pip install pycdlib unicorn capstone
    if errorlevel 1 goto :pip_failed
)

if exist "!ISO_PT!" (
    echo Apagando ISO PT antiga...
    del /Q "!ISO_PT!"
)

echo Copiando ISO original pra ISO PT (1.3GB, leva ~10 segundos)...
copy /Y /B "!ORIG!" "!ISO_PT!" >nul
if errorlevel 1 goto :copy_failed

echo.
echo [1/4] Aplicando traducoes em SYSTEM.MSG e SI_*.DAT...
python "tools\ilhm_build.py" --iso "!ISO_PT!" --work "work"
if errorlevel 1 goto :build_failed

echo.
echo [2/4] Corrigindo labels de UI/status nao-escaneadas (SI_MN00/02)...
python "tools\patch_mn_ui.py" --iso "!ISO_PT!" --apply
if errorlevel 1 goto :build_failed

echo.
echo [3/4] Recompilando .SCP traduzidos (pode demorar varios minutos)...
python "tools\scp_pipeline.py" build --work "work"
if errorlevel 1 goto :build_failed

echo.
echo [4/4] Aplicando .SCP recompilados na ISO...
python "tools\scp_iso_patch.py" --iso "!ISO_PT!" --work "work"
if errorlevel 1 goto :build_failed

echo.
echo Pronto. Abre no PCSX2: %CD%\!ISO_PT!
pause
exit /b 0

:orig_missing
echo ERRO: ISO original nao encontrada em:
echo   %CD%\!ORIG!
pause
exit /b 1

:no_python
echo ERRO: 'python' nao encontrado no PATH.
echo Instale Python e marca "Add Python to PATH": https://www.python.org/downloads/
pause
exit /b 1

:pip_failed
echo Falha ao instalar dependencias. Tenta manualmente:
echo   python -m pip install pycdlib unicorn capstone
pause
exit /b 1

:copy_failed
echo Falha ao copiar ISO.
pause
exit /b 1

:build_failed
echo Build falhou. ISO PT pode estar inconsistente.
pause
exit /b 1
