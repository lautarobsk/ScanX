@echo off
title Sistema ALPR - Centro de Monitoreo Policial
color 0A

echo ======================================================================
echo    SISTEMA DE MONITOREO POLICIAL Y RASTREO VEHICULAR (ALPR)
echo ======================================================================
echo.

set "ROOT=%~dp0"

echo [1/3] Iniciando Servidor Backend (Django REST Framework en puerto 8000)...
start "Backend Django API" cmd /k "cd /d "%ROOT%" && call venv\Scripts\activate.bat && python manage.py runserver"

timeout /t 3 /nobreak > nul

echo [2/3] Iniciando Centro de Monitoreo (React + Vite en puerto 5173)...
start "Frontend React Dashboard" cmd /k "cd /d "%ROOT%dashboard-policial" && npm run dev"

timeout /t 3 /nobreak > nul

echo [3/3] Abriendo Centro de Monitoreo en el navegador...
start http://localhost:5173

echo.
echo ======================================================================
echo  Servidores iniciados con exito.
echo.
echo  Para ejecutar el nodo de Vision Artificial (Deteccion ALPR):
echo  1. Abrir terminal en: sandbox-vision
echo  2. Activar venv: venv\Scripts\activate
echo  3. Ejecutar: python demostrador.py
echo ======================================================================
pause
