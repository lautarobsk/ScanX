import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const MapaView = () => {
  const posicion = [-28.4696, -65.7852]; //SFVC

  return (
    <MapContainer
      center={posicion}
      zoom={13}
      style={{ height: "1440px", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.esri.com/">Esri</a>'
        url="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}"
      />

      <Marker position={posicion}>
        <Popup>¡Hola!</Popup>
      </Marker>
    </MapContainer>
  );
};

export default MapaView;
