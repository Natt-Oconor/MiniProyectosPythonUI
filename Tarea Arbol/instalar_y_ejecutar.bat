@echo off
chcp 65001 >nul 2>&1
title Unidad 9 - Arboles BST
setlocal EnableDelayedExpansion
cd /d "%~dp0"

rem Detectar el lanzador de Python (py -3 o python)
set "PY="
where py >nul 2>&1
if not errorlevel 1 set "PY=py -3"
if not defined PY (
  where python >nul 2>&1
  if not errorlevel 1 set "PY=python"
)

:menu
cls
echo ================================================================
echo    UNIDAD 9: ARBOLES - INSTALACION Y EJECUCION DE ACTIVIDADES
echo    Carpeta: %~dp0
echo ================================================================
echo.
echo    1. Verificar / Instalar Python 3
echo    2. Ejemplos resueltos         (ejemplos.py)
echo    3. Tarea - 5 metodos BST      (demo_tarea.py)
echo    4. Mini-Proyecto Diccionario  (diccionario_inteligente.py)
echo    5. Ejecutar TODAS las actividades en secuencia
echo    6. Salir
echo.
set "opc="
set /p opc=  Seleccione una opcion [1-6]:

if "%opc%"=="1" goto instalar
if "%opc%"=="2" goto ejemplos
if "%opc%"=="3" goto tarea
if "%opc%"=="4" goto mini
if "%opc%"=="5" goto todas
if "%opc%"=="6" goto fin
echo.
echo  Opcion no valida.
pause
goto menu

:instalar
cls
echo ================================================================
echo    VERIFICACION / INSTALACION DE PYTHON 3
echo ================================================================
echo.
if defined PY (
  echo  Python detectado:
  !PY! --version
  echo.
  echo  Ya tiene Python instalado. No se requiere nada mas.
  pause
  goto menu
)
echo  Python NO encontrado en el sistema.
echo.
echo  Intentando instalar con winget (requiere Windows 10/11 con App Installer)...
where winget >nul 2>&1
if errorlevel 1 (
  echo.
  echo  No se encontro winget. Instale Python manualmente desde:
  echo      https://www.python.org/downloads/
  echo  Durante la instalacion marque la casilla:
  echo      [x] Add python.exe to PATH
  echo.
  pause
  goto menu
)
winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements
echo.
echo  Instalacion finalizada.
echo  CIERRE esta ventana, vuelva a abrir el .bat y use la opcion 1
echo  para confirmar. Luego ejecute las actividades (opciones 2-5).
pause
goto menu

:ejemplos
cls
echo ================================================================
echo    EJEMPLOS RESUELTOS (seccion 4 del U9_arboles.md)
echo ================================================================
if not defined PY (
  echo  Python no esta instalado. Use la opcion 1.
  pause
  goto menu
)
echo.
!PY! "%~dp0ejemplos.py"
echo.
pause
goto menu

:tarea
cls
echo ================================================================
echo    TAREA / HOMEWORK - 5 METODOS BST (seccion 6 del U9_arboles.md)
echo    1) eliminar  2) BFS  3) suma  4) es_completo  5) balancear
echo ================================================================
if not defined PY (
  echo  Python no esta instalado. Use la opcion 1.
  pause
  goto menu
)
echo.
!PY! "%~dp0demo_tarea.py"
echo.
pause
goto menu

:mini
cls
echo ================================================================
echo    MINI-PROYECTO: DICCIONARIO INTELIGENTE (seccion 7)
echo ================================================================
if not defined PY (
  echo  Python no esta instalado. Use la opcion 1.
  pause
  goto menu
)
echo.
echo  Inicie sesion interactiva. Opciones del menu:
echo  1 = buscar palabra exacta   2 = autocompletar por prefijo
echo  3 = diccionario A-Z         4 = estadisticas   5 = salir
echo.
!PY! "%~dp0diccionario_inteligente.py"
echo.
pause
goto menu

:todas
cls
echo ================================================================
echo    EJECUCION SECUENCIAL DE TODAS LAS ACTIVIDADES
echo ================================================================
if not defined PY (
  echo  Python no esta instalado. Use la opcion 1.
  pause
  goto menu
)
echo.
echo  --- [1/3] Ejemplos resueltos ---
echo.|!PY! "%~dp0ejemplos.py"
echo.
echo  --- [2/3] Tarea (5 metodos BST) ---
echo.|!PY! "%~dp0demo_tarea.py"
echo.
echo  --- [3/3] Mini-Proyecto Diccionario (demo no interactiva: se omite) ---
echo  El diccionario es interactivo; ejecute la opcion 4 para usarlo.
echo.
echo  TODAS LAS ACTIVIDADES FINALIZADAS.
pause
goto menu

:fin
echo.
echo  Hasta luego.
exit /b 0
