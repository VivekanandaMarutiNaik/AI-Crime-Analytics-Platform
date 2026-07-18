import {
  MapContainer,
  TileLayer,
  Popup,
  CircleMarker,
  GeoJSON,
  useMap,
  useMapEvents,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import MarkerClusterGroup from "react-leaflet-cluster";

import { useEffect, useState } from "react";

import {
  getCrimes,
  getHotspots,
  getExistingCCTV,
  getRecommendedCCTV,
} from "../services/api";

import L from "leaflet";

function FlyToDistrict({ crimes, district }) {
  const map = useMap();

  useEffect(() => {
    if (!district || crimes.length === 0) return;
    
    const points = crimes
      .filter(
        (crime) =>
          crime.crime_latitude != null &&
          crime.crime_longitude != null
      )
      .map((crime) => [
        Number(crime.crime_latitude),
        Number(crime.crime_longitude),
      ]);

    if (points.length === 0) return;

    const bounds = L.latLngBounds(points);

    map.fitBounds(bounds, {
      padding: [50, 50],
      animate: true,
      duration: 1.5,
    });

    
  }, [district, crimes, map]);

  return null;
}


function SetKarnatakaView() {
  const map = useMap();

  useEffect(() => {
    const bounds = L.latLngBounds(
      [11.3, 73.8], // South-West
      [18.7, 78.9]  // North-East
    );

    map.fitBounds(bounds);
  }, [map]);

  return null;
}

function getSeverityColor(severity) {
  switch (severity) {
    case "Critical":
      return "#d32f2f";
    case "High":
      return "#f57c00";
    case "Medium":
      return "#fbc02d";
    default:
      return "#2e7d32";
  }
}

function getRiskLevel(count) {
  if (count >= 40) return "Critical";
  if (count >= 25) return "High";
  if (count >= 15) return "Medium";
  return "Low";
}

function getRiskColor(level) {
  switch (level) {
    case "Critical":
      return "#d32f2f";
    case "High":
      return "#f57c00";
    case "Medium":
      return "#fbc02d";
    default:
      return "#2e7d32";
  }
}

function getAIInsight(severity) {
  switch (severity) {
    case "Critical":
      return "Immediate police response and CCTV surveillance recommended.";
    case "High":
      return "Increase patrol frequency and monitor suspicious activity.";
    case "Medium":
      return "Regular monitoring recommended.";
    default:
      return "Routine observation is sufficient.";
  }
}
function MapLegend() {
  const map = useMap();

  useEffect(() => {
    const legend = L.control({ position: "bottomright" });

    legend.onAdd = function () {
      const div = L.DomUtil.create("div");

      div.style.background = "white";
      div.style.padding = "10px";
      div.style.borderRadius = "8px";
      div.style.boxShadow = "0 2px 8px rgba(0,0,0,0.3)";
      div.style.fontSize = "13px";

      div.innerHTML = `
        <b>Map Legend</b><br><br>
        🟠 Crime<br>
        🔥 Hotspot<br>
        🔵 Existing CCTV<br>
        🟢 AI Recommendation
      `;

      return div;
    };

    legend.addTo(map);

    return () => map.removeControl(legend);
  }, [map]);

  return null;
}

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
  const [districtGeoJSON, setDistrictGeoJSON] = useState(null);

  useEffect(() => {
    getCrimes(500, district)
  .then((data) => {
    console.log("Crime API returned:", data.length);
console.log(data.slice(0, 5));
    console.log("Crime records from API:", data.length);

    setCrimes(data);
  })
  .catch(console.error);

    getHotspots(district)
      .then(setHotspots)
      .catch(console.error);

    getExistingCCTV(district)
  .then((data) => {
    setCctvs(data);
    console.log("First 20 CCTV");
console.table(
  data.slice(0,20).map(c => ({
    id: c.cctv_id,
    lat: c.latitude,
    lon: c.longitude
  }))
);
    console.log("District:", district);
    console.log("CCTV Count:", data.length);

    data.forEach((c) => {
      if (
        c.longitude > 78.9 ||
        c.longitude < 73.8 ||
        c.latitude > 18.7 ||
        c.latitude < 11.3
      ) {
        console.log(
          "BAD CCTV:",
          c.cctv_id,
          c.latitude,
          c.longitude,
          c.district
        );
      }
    });
  })
  .catch(console.error);

    getRecommendedCCTV(district)
  .then((data) => {
    console.log("Recommendations:", district, data.length);
    console.log(data.slice(0, 5));
    setRecommendedCCTVs(data);
  })
  .catch(console.error);

    fetch("/maps/karnataka_districts.geojson")
  .then((res) => res.json())
  .then(setDistrictGeoJSON)
  .catch(console.error);
  }, [district]);

  console.log("Crime markers being rendered:", crimes.length);
console.log("Rendering...");
console.log("Crimes:", crimes.length);
console.log("CCTV:", cctvs.length);
console.log("Recommendations:", recommendedCCTVs.length);
console.log("Hotspots:", hotspots.length);
  return (
    <MapContainer

    
      center={[15.3173, 75.7139]}
      zoom={8}
      minZoom={7}
      maxZoom={18}
      scrollWheelZoom={true}
      
      maxBounds={[
        [11.3, 73.8],
        [18.7, 78.9],
      ]}
      maxBoundsViscosity={1.0}
     style={{
  height: "650px",
  width: "100%",
  borderRadius: "12px",
  overflow: "hidden",
}}

    >
      <TileLayer
        attribution="© OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <SetKarnatakaView />
      <MapLegend />

      <FlyToDistrict
        crimes={crimes}
        district={district}
      />

      {/* Crime Markers */}
{showCrimes && (
  <MarkerClusterGroup
    chunkedLoading
    maxClusterRadius={45}
  >
  {crimes.map((crime) => {
  console.log(
    crime.crime_id,
    crime.crime_latitude,
    crime.crime_longitude
  );

  return (
    <CircleMarker
      skey={crime.crime_id}
      center={[
        Number(crime.crime_latitude),
        Number(crime.crime_longitude),
      ]}
      radius={6}
      pathOptions={{
        color: "red",
        fillColor: "red",
        fillOpacity: 1,
      }}
    />
  );
})}
  </MarkerClusterGroup>
)}
      {/* Existing CCTV */}
{showCCTV && (
  <>
    {cctvs.map((camera) => (
      <CircleMarker
        key={camera.cctv_id}
        center={[
          Number(camera.latitude),
          Number(camera.longitude),
        ]}
        radius={4}
        pathOptions={{
          color: "#1976d2",
          fillColor: "#1976d2",
          fillOpacity: 0.9,
        }}
      >
        <Popup>
          <b>{camera.cctv_name}</b>
          <br />
          Status: {camera.status}
          <br />
          Coverage: {camera.coverage_radius_meters} m
          <br />
          Police Station: {camera.nearest_police_station}
        </Popup>
      </CircleMarker>
    ))}
  </>
)}
      {/* AI Recommended CCTV */}
{showRecommendations && (
  <>
    {recommendedCCTVs.map((rec) => (
      <CircleMarker
        key={`${rec.village_id}-${rec.latitude}-${rec.longitude}`}
        center={[
          Number(rec.latitude),
          Number(rec.longitude),
        ]}
        radius={6}
        pathOptions={{
          color: "#2e7d32",
          fillColor: "#2e7d32",
          fillOpacity: 0.9,
        }}
      >
        <Popup>
          Village: {rec.village}
          <br />
          Priority: {rec.priority}
        </Popup>
      </CircleMarker>
    ))}
  </>
)}
      {/* Hotspots */}
      {showHotspots &&
        hotspots.map((spot, index) => (
          <CircleMarker
            key={index}
            center={[
              Number(spot.latitude),
              Number(spot.longitude),
            ]}
            radius={10}
            pathOptions={{
              color: "#ff5722",
              fillColor: "#ff5722",
             fillOpacity: 0.35,
            }}
          >
            <Popup minWidth={260}>
  <div style={{ lineHeight: "1.7" }}>
    <h3
      style={{
        margin: 0,
        color: "#e65100",
      }}
    >
      🔥 Crime Hotspot
    </h3>

    <hr />

    <b>District:</b> {spot.district}<br />
    <b>Taluk:</b> {spot.taluk}<br />

    <b>Total Cases:</b> {spot.crime_count}<br />

    <b>Risk Level:</b>{" "}
    <span
      style={{
        color: getRiskColor(
          getRiskLevel(spot.crime_count)
        ),
        fontWeight: "bold",
      }}
    >
      {getRiskLevel(spot.crime_count)}
    </span>

    <br />

    <b>Suggested CCTV:</b>{" "}
    {spot.recommended_cctv}

    <hr />

    <div
      style={{
        color: "#1976d2",
      }}
    >
      AI recommends increasing surveillance in this area.
    </div>
  </div>
</Popup>
          </CircleMarker>
          
        ))}
       {districtGeoJSON && (
  <GeoJSON
    data={districtGeoJSON}
    style={() => ({
  color: "#c62828",
  weight: 2,
  fillColor: "#fff8b5",
  fillOpacity: 0.15,
})}
    onEachFeature={(feature, layer) => {

  layer.on({
    mouseover: (e) => {
      e.target.setStyle({
        weight: 3,
        fillOpacity: 0.35,
      });
    },

    mouseout: (e) => {
      e.target.setStyle({
        weight: 2,
        fillOpacity: 0.15,
      });
    },
  });

  layer.bindPopup(
    `<b>${feature.properties.district_name}</b>`
  );
}}
  />
)}
    </MapContainer>
  );
}

export default CrimeMap;