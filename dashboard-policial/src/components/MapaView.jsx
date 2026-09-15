import React, { useState, useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./MapaView.css";
import markerIconPng from "leaflet/dist/images/marker-icon.png";
import markerShadowPng from "leaflet/dist/images/marker-shadow.png";
import axios from "axios";

let DefaultIcon = L.icon({
  iconUrl: markerIconPng,
  shadowUrl: markerShadowPng,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});
L.Marker.prototype.options.icon = DefaultIcon;

const MapaView = () => {
  const posicionCatamarca = [-28.4695, -65.7801];

  const [historial, setHistorial] = useState([]);
  const patenteBuscada = "AB123CD";

  const [camaras, setCamaras] = useState([]);

const [mostrarRuta, setMostrarRuta] = useState(true);
const [mostrarCamaras, setMostrarCamaras] = useState(true);


  useEffect(() => {
    const token = import.meta.env.VITE_API_TOKEN;
    const configSeguridad = {
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    };

    const pedirDatosADjango = async () => {
      try {
        const respuesta = await axios.get(
          `http://127.0.0.1:8000/api/tracker/historial/${patenteBuscada}/`,
          configSeguridad,
        );
        setHistorial(respuesta.data);
      } catch (error) {
        console.error(
          "Error al pedir historial:",
          error.response ? error.response.data : error.message,
        );
      }
    };

    const getCamaras = async () => {
      try {
        const respuesta = await axios.get(
          "http://127.0.0.1:8000/api/tracker/getCamaras/",
          configSeguridad,
        );
        setCamaras(respuesta.data);
      } catch (error) {
        console.error(
          "Error al pedir cámaras:",
          error.response ? error.response.data : error.message,
        );
      }
    };

    pedirDatosADjango();
    getCamaras();
    const radar = setInterval(pedirDatosADjango, 25000);
    return () => clearInterval(radar);
  }, []);

  // Aca filtro las coordenadas y luego lo guardo en un nuevo array para poder dibujar las polilinea
  const coordenadasRuta = historial
    .filter((registro) => registro.latitud && registro.longitud)
    .map((registro) => [registro.latitud, registro.longitud]);

  const iconoTactico = L.divIcon({
    className: "punto-tactico",
    html: "",
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  });

  const iconoCamara = L.divIcon({
    className: "icono-camara",
    html: "",
    iconSize: [12, 12],
    iconAnchor: [6, 6],
  });

  return (
    <div className="dashboard-container">
      <div className="sidebar">
        <h2 style={{ margin: "0 0 20px 0", fontSize: "22px" }}>Centro de Monitoreo</h2>

        <label style={{ display: 'flex', alignItems: 'center', marginBottom: '10px', cursor: 'pointer' }}>
            <input 
              type="checkbox" 
              checked={mostrarRuta} 
              onChange={() => setMostrarRuta(!mostrarRuta)} 
              style={{ marginRight: '10px', width: '16px', height: '16px' }}
            />
            Ver Nodos
          </label>

          <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
            <input 
              type="checkbox" 
              checked={mostrarCamaras} 
              onChange={() => setMostrarCamaras(!mostrarCamaras)} 
              style={{ marginRight: '10px', width: '16px', height: '16px' }}
            />
            Ver Cámaras
          </label>
      
        <div className="panel-info">
          <h3>Sospechoso</h3>
          <p><strong>Patente:</strong> {patenteBuscada}</p>
          <p><strong>Estado:</strong> Rastreo Automático</p>
        </div>
      
        <div className="panel-info">
          <h3>Última Detección</h3>
          {historial.length > 0 ? (
            <>
              <p><strong>Cámara:</strong> {historial[historial.length - 1].camara_codigo}</p>
              <p><strong>Dirección: </strong> {historial[historial.length - 1].direccion}</p>
              <p><strong>Hora:</strong> {new Date(historial[historial.length - 1].timestamp).toLocaleTimeString("es-AR")}</p>
            </>
          ) : (
            <p style={{ color: "#888" }}>Sin detecciones recientes...</p>
          )}
        </div>

        <div className="panel-info">
          <h3>Cámaras</h3>
          <p><strong>Operativas:</strong> {camaras.length} nodos conectados</p>
        </div>

      </div>

      <div className="mapa-wrapper">
        <MapContainer
          center={posicionCatamarca}
          zoom={14}
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            attribution="&copy; OpenStreetMap contributors"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            className="mapa-oscuro"
          />

          {mostrarRuta && historial.map((registro) =>
            registro.latitud && registro.longitud ? (
              <Marker
                key={registro.id}
                position={[registro.latitud, registro.longitud]}
                icon={iconoTactico}
              >
                <Popup>
                  <strong>Cámara:</strong> {registro.camara_codigo} <br />
                  <strong>Hora:</strong>{" "}
                  {new Date(registro.timestamp).toLocaleTimeString("es-AR")}
                </Popup>
              </Marker>
            ) : null,
          )}

          {mostrarCamaras && camaras.map((camara) =>
            camara.latitud && camara.longitud ? (
              <Marker
                key={camara.codigo_identificador}
                position={[camara.latitud, camara.longitud]}
                icon={iconoCamara}
              >
                <Popup>
                  <strong>Cámara:</strong> {camara.codigo_identificador} <br />
                  <strong>Estado:</strong>{" "}
                  {camara.activa ? "🟢 Activa" : "🔴 Inactiva"} <br />
                  <strong>Dirección:</strong> {camara.direccion}
                </Popup>
              </Marker>
            ) : null,
          )}

          <Polyline
            positions={coordenadasRuta}
            color="red"
            weight={4}
            dashArray="10, 10"
          />
        </MapContainer>
      </div>
    </div>
  );
};

export default MapaView;
