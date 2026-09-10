import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import markerIconPng from "leaflet/dist/images/marker-icon.png";
import markerShadowPng from "leaflet/dist/images/marker-shadow.png";
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

  useEffect(() => {
    const pedirDatosADjango = async () => {
      try {
        const respuesta = await fetch(
          `http://127.0.0.1:8000/api/tracker/historial/${patenteBuscada}/`,
        );
        if (respuesta.ok) {
          const datos = await respuesta.json();
          setHistorial(datos);
        }
      } catch (error) {
        console.error("Error al intentar hablar con Django:", error);
      }
    };

    pedirDatosADjango();
    const radar = setInterval(pedirDatosADjango, 9000);
    return () => clearInterval(radar);
  }, []);

  // Aca filtro coordenadas y luego lo guardo en un nuevo array para poder dibujar las polilinea
  const coordenadasRuta = historial
    .filter((registro) => registro.latitud && registro.longitud)
    .map((registro) => [registro.latitud, registro.longitud]);

  return (
    <div
      style={{
        height: "1440px",
        width: "100%",
        borderRadius: "8px",
        overflow: "hidden",
      }}
    >
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

        {historial.map((registro) =>
          registro.latitud && registro.longitud ? (
            <Marker
              key={registro.id}
              position={[registro.latitud, registro.longitud]}
            >
              <Popup>
                <strong>Cámara:</strong> {registro.camara_codigo} <br />
                <strong>Hora:</strong>{" "}
                {new Date(registro.timestamp).toLocaleTimeString("es-AR")}
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
  );
};

export default MapaView;
