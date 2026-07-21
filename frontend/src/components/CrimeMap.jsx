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
  console.log("District:", district);
  console.log("Crime count:", crimes.length);

  if (crimes.length === 0) return;

  const points = crimes
    .filter(
      (c) =>
        c.crime_latitude !== null &&
        c.crime_longitude !== null
    )
    .map((c) => [
      Number(c.crime_latitude),
      Number(c.crime_longitude),
    ]);

  console.log("Points:", points.length);

  if (points.length === 0) return;
const bounds = L.latLngBounds(points);

console.log("Bounds:", bounds.toBBoxString());
console.log("North:", bounds.getNorth());
console.log("South:", bounds.getSouth());
console.log("East:", bounds.getEast());
console.log("West:", bounds.getWest());

map.fitBounds(bounds, {
  padding: [40, 40],
  animate: true,
});
  
}, [crimes, district, map]);
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

function getRecommendationColor(priority) {
  switch (priority) {
    case "Critical":
      return "#d32f2f"; // Red
    case "High":
      return "#f57c00"; // Orange
    case "Medium":
      return "#fbc02d"; // Yellow
    default:
      return "#2e7d32"; // Green
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
  onHotspotSelect,
}) {
  const [crimes, setCrimes] = useState([]);
  const [hotspots, setHotspots] = useState([]);
  const [cctvs, setCctvs] = useState([]);
  const [recommendedCCTVs, setRecommendedCCTVs] = useState([]);
  const [districtGeoJSON, setDistrictGeoJSON] = useState(null);

  useEffect(() => {
  getCrimes(5000, district)
  .then((data) => {
    console.log("Crime API returned:", data);

    console.table(
  data.slice(0, 20).map(c => ({
    case: c.case_id,
    district: c.district,
    taluk: c.taluk,
    village: c.village,
    lat: c.crime_latitude,
    lon: c.crime_longitude,
  }))
);

setCrimes(data);
  })
  .catch(console.error);

    getHotspots(district)
  .then((data) => {
    console.log("Hotspots API:", data);

    console.table(
      data.map((h) => ({
        district: h.district,
        taluk: h.taluk,
        lat: h.latitude,
        lon: h.longitude,
      }))
    );

    setHotspots(data);
  })
  .catch(console.error);

    getExistingCCTV(district)
  .then((data) => {
    setCctvs(data);
    console.log(
  "CCTV Latitude:",
  Math.min(...data.map(c => Number(c.latitude))),
  "->",
  Math.max(...data.map(c => Number(c.latitude)))
);

console.log(
  "CCTV Longitude:",
  Math.min(...data.map(c => Number(c.longitude))),
  "->",
  Math.max(...data.map(c => Number(c.longitude)))
);
console.log("First 20 CCTV");

console.table(
  data.slice(0, 20).map(c => ({
    id: c.cctv_id,
    lat: c.latitude,
    lon: c.longitude,
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
console.log("CrimeMap received district:", district);

console.table(
  crimes.slice(0, 20).map(c => ({
    village: c.village,
    lat: c.crime_latitude,
    lon: c.crime_longitude,
  }))
);
const lats = crimes.map(c => Number(c.crime_latitude));
const lons = crimes.map(c => Number(c.crime_longitude));

console.log("Latitude range:", Math.min(...lats), "->", Math.max(...lats));
console.log("Longitude range:", Math.min(...lons), "->", Math.max(...lons));
console.table(
  recommendedCCTVs.slice(0, 10).map(r => ({
    village: r.village,
    lat: Number(r.latitude),
    lon: Number(r.longitude),
  }))
);

console.log("Selected district:", district);
const DISPLAY_LIMIT = 500;

const displayedCrimes = crimes;
console.log("Displayed crimes:", displayedCrimes.length);

displayedCrimes.forEach(c => {
  if (
    c.crime_latitude < 15.2 ||
    c.crime_latitude > 17.7 ||
    c.crime_longitude < 75.2 ||
    c.crime_longitude > 77.8
  ) {
    console.log("OUTSIDE:", c);
  }
});
const badCoords = displayedCrimes.filter(c => {
  const lat = Number(c.crime_latitude);
  const lon = Number(c.crime_longitude);

  return (
    lat < 15.2 ||
    lat > 17.7 ||
    lon < 75.2 ||
    lon > 77.8
  );
});

console.log("Bad coordinate crimes:", badCoords);
console.log(
  "Wrong district crimes:",
  displayedCrimes.filter(
    c => c.district !== district
  )
);
  return (
    <MapContainer
  key={district || "all"}

    
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
  <>
    {displayedCrimes.map((crime) => (
      <CircleMarker
        key={crime.case_id}
        center={[
          Number(crime.crime_latitude),
          Number(crime.crime_longitude),
        ]}
        radius={10}
        pathOptions={{
          color: "red",
          fillColor: "red",
          fillOpacity: 0.7,
        }}
      >
        <Popup>
  <b>{crime.district}</b><br />
  {crime.taluk}<br />
  {crime.village}<br />
  Lat: {crime.crime_latitude}<br />
  Lon: {crime.crime_longitude}
</Popup>
      </CircleMarker>
    ))}
  </>
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
  <b>Existing CCTV</b><br />
  District: {camera.district}<br />
  Taluk: {camera.taluk}<br />
  Police Station: {camera.police_station}<br />
  Lat: {camera.latitude}<br />
  Lon: {camera.longitude}
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
  color: getRecommendationColor(rec.priority),
  fillColor: getRecommendationColor(rec.priority),
  fillOpacity: 0.9,
}}
      >
        <Popup>
  <b>📍 {rec.village}</b>
  <br />
  District: {rec.district}
  <br />
  Taluk: {rec.taluk}
  <br />
  Crimes: {rec.crime_count}
  <br />
  Priority: <b>{rec.priority}</b>
  <br />
  AI Recommendation:{" "}
  {rec.recommend_installation ? "Install CCTV" : "No Installation Needed"}
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
            radius={14}
            pathOptions={{
              color: "#ff5722",
              fillColor: "#ff5722",
             fillOpacity: 0.2,
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
    <br />

<button
  onClick={() =>
    onHotspotSelect?.({
      district: spot.district,
      taluk: spot.taluk,
      crimeCount: spot.crime_count,
      riskLevel: getRiskLevel(spot.crime_count),
      recommendedCCTV: spot.recommended_cctv,
    })
  }
>
  🤖 Analyze with AI
</button>
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