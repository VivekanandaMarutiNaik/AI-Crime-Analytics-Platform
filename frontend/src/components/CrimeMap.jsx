import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  CircleMarker,
  Circle,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

import { useEffect, useState } from "react";

import {
  getCrimes,
  getHotspots,
  getExistingCCTV,
  getRecommendedCCTV,
} from "../services/api";

function CrimeMap({
  district,
  showCrimes,
  showHotspots,
  showCCTV,
  showRecommendations,
}) {
  const [crimes, setCrimes] = useState([]);

  const [hotspots, setHotspots] = useState([]);
  const [cctvs, setCctvs] = useState([]);
  const [recommendedCCTVs, setRecommendedCCTVs] = useState([]);

  useEffect(() => {
    getCrimes(100, district)
      .then((data) => {
        setCrimes(data);
      })
      .catch((error) => console.error(error));

    getHotspots(district)
      .then((data) => {
        setHotspots(data);
      })
      .catch((error) => console.error(error));

    getExistingCCTV(district)
        .then((data) => {
            setCctvs(data);
        })
        .catch((error) => console.error(error));

    getRecommendedCCTV(district)
        .then((data) => {
            setRecommendedCCTVs(data);
        })
        .catch((error) => console.error(error));
  }, [district]);

  console.log("Recommendations:", recommendedCCTVs.length);

  return (
    <MapContainer
      center={[15.3173, 75.7139]}
      zoom={7}
      style={{
        height: "600px",
        width: "100%",
        borderRadius: "12px",
        marginTop: "20px",
      }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {showCrimes &&
        crimes.map((crime) => (
          <Marker
            key={crime.crime_id}
            position={[
              crime.crime_latitude,
              crime.crime_longitude,
            ]}
          >
            <Popup>
              <strong>{crime.crime_type}</strong>
              <br />
              District: {crime.district}
              <br />
              Police Station: {crime.police_station_name}
              <br />
              Severity: {crime.crime_severity}
            </Popup>
          </Marker>
        ))}

      {showHotspots &&
        hotspots.map((hotspot) => (
          <CircleMarker
            key={hotspot.cluster}
            center={[
              hotspot.latitude,
              hotspot.longitude,
            ]}
            radius={Math.min(
              8 + hotspot.crime_count / 20,
              25
            )}
            pathOptions={{
              color: "red",
              fillColor: "red",
              fillOpacity: 0.5,
            }}
          >
            <Popup>
              <strong>Crime Hotspot</strong>
              <br />
              Cluster: {hotspot.cluster}
              <br />
              Crimes: {hotspot.crime_count}
              <br />
              Recommended CCTV:{" "}
              {hotspot.recommended_cctv}
            </Popup>
          </CircleMarker>
        ))}
        {showCCTV &&
            cctvs.map((camera) => (
              <CircleMarker
                key={camera.cctv_id}
                center={[camera.latitude, camera.longitude]}
                radius={5}
                pathOptions={{
                    color: "#1976d2",
                    fillColor: "#1976d2",
                    fillOpacity: 0.9,
                }}
                >
                <Popup>
                    <strong>{camera.cctv_name}</strong>
                    <br />
                    Police Station: {camera.nearest_police_station}
                    <br />
                    Coverage Radius: {camera.coverage_radius_meters} m
                    <br />
                    Status: {camera.status}
                </Popup>
              </CircleMarker>
        ))}

        {showRecommendations &&
            recommendedCCTVs.map((camera) => {
                console.log("Recommendation object:", camera);

                return (
                <CircleMarker
                    key={camera.cluster}
                    center={[Number(camera.latitude), Number(camera.longitude)]}
                    radius={12}
                    pathOptions={{
                    color: "#00ff00",
                    fillColor: "#00ff00",
                    fillOpacity: 1,
                    weight: 4,
                    }}
                >
                    <Popup>
                    <strong>Cluster {camera.cluster}</strong>
                    </Popup>
                </CircleMarker>
                );
        })}


    </MapContainer>
  );
}

export default CrimeMap;