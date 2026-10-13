# Sistema de Monitoreo Policial y Rastreo Vehicular (ALPR)

Sistema integral de seguridad distribuido compuesto por:
1. **Backend:** Django REST Framework con base de datos SQLite y motor de prediccion de escape.
2. **Frontend:** Centro de Monitoreo en React + Leaflet con visualizacion cartografica en tiempo real.
3. **Vision Artificial:** Deteccion y lectura de patentes (YOLOv8 + EasyOCR + Algoritmo de Consenso).

---

## Como iniciar el proyecto en otra computadora

### Requisitos previos
- Python 3.10 o superior instalado (marcar la casilla "Add Python to PATH" durante la instalacion).
- Node.js 18 o superior instalado.
- Git instalado.

---

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/lautarobsk/ScanX.git
cd ScanX
```

---

### Paso 2: Configurar el Backend (Django)
En la carpeta raiz del proyecto:
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```
El servidor backend estara corriendo en `http://127.0.0.1:8000`.

---

### Paso 3: Configurar el Centro de Monitoreo (React)
En una nueva terminal:
```powershell
cd dashboard-policial
npm install
npm run dev
```
Abrir el navegador en `http://localhost:5173`.

---

### Paso 4: Configurar y ejecutar la Vision Artificial
En una nueva terminal:
```powershell
cd sandbox-vision
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python demostrador.py
```
O para ejecutar la deteccion de video directamente:
```powershell
cd pruebas
python video_deteccion.py
```

---

### Inicio Rapido con Lanzador (Windows)
Una vez instaladas las dependencias, podes hacer doble clic en `iniciar_proyecto.bat` en la raiz del proyecto para iniciar el backend, frontend y navegador en un solo paso.
