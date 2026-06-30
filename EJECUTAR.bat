@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
title FastDelivery Agents - CortexGovernor Academy

REM Verificar que Python existe
python --version >nul 2>nul
if errorlevel 1 (
  echo.
  echo [ERROR] No se encontro Python.
  echo Instalalo desde https://www.python.org/downloads/ y marca "Add Python to PATH".
  echo.
  pause
  exit /b
)

:menu
cls
echo ============================================================
echo    FastDelivery Agents  -  CortexGovernor Academy
echo ============================================================
echo.
echo    1. Instalar dependencias (hazlo la PRIMERA vez)
echo    2. Configurar mi API key (opcional - activa el LLM)
echo    3. Probar el asistente (3 ejemplos)
echo    4. Correr las pruebas
echo    5. Generar y ABRIR el tablero (board_sync)
echo    6. Hacer mi propia pregunta
echo    7. Salir
echo.
set /p op="Elige una opcion (1-7) y pulsa Enter: "

if "%op%"=="1" goto install
if "%op%"=="2" goto setkey
if "%op%"=="3" goto demo
if "%op%"=="4" goto test
if "%op%"=="5" goto board
if "%op%"=="6" goto ask
if "%op%"=="7" goto end
goto menu

:install
echo.
echo Instalando dependencias (anthropic, pytest)...
python -m pip install -r requirements.txt
echo.
echo Listo. Ya puedes usar las opciones 3, 4 y 5.
pause
goto menu

:setkey
echo.
echo Pega tu API key de Anthropic (empieza con sk-ant-...).
echo Si no tienes, deja vacio y pulsa Enter: el sistema funciona igual sin LLM.
echo.
set /p k="API key: "
if "%k%"=="" (
  echo.
  echo No se configuro key. Seguira en modo sin LLM ^(plantillas^).
  pause
  goto menu
)
>.env echo ANTHROPIC_API_KEY=%k%
echo.
echo Guardada en el archivo .env. Las opciones 3 y 6 ahora usaran el LLM.
pause
goto menu

:demo
echo.
python -m src.main "donde esta mi pedido A1001"
python -m src.main "tienen pizza hawaiana"
python -m src.main "quiero un reembolso de 40 soles del pedido A1002"
echo.
pause
goto menu

:test
echo.
python -m pytest -q
echo.
pause
goto menu

:board
echo.
python board_sync.py
echo.
echo Abriendo SPRINT_BOARD.html en el navegador...
start "" "SPRINT_BOARD.html"
echo.
pause
goto menu

:ask
echo.
set /p q="Escribe tu pregunta: "
echo.
python -m src.main "%q%"
echo.
pause
goto menu

:end
echo.
echo Hasta luego.
