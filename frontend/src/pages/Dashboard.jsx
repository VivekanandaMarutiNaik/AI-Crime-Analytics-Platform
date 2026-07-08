import { useEffect, useState } from "react";
import {
  getDashboardSummary,
  getDistricts,
  getDashboardCharts,
  getAIInsights,
} from "../services/api";
import {
  Container,
  Typography,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  Box,
} from "@mui/material";
import CrimeSeverityChart from "../components/CrimeSeverityChart";
import CrimeTypeChart from "../components/CrimeTypeChart";
import DistrictChart from "../components/DistrictChart";
import AIInsightsCard from "../components/AIInsightsCard";

import SummaryCard from "../components/SummaryCard";
import CrimeMap from "../components/CrimeMap";

import GavelIcon from "@mui/icons-material/Gavel";
import VideocamIcon from "@mui/icons-material/Videocam";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import SecurityIcon from "@mui/icons-material/Security";

function Dashboard() {
  const [summary, setSummary] = useState(null);

  const [selectedDistrict, setSelectedDistrict] = useState("");

  const [districts, setDistricts] = useState([]);

  const [showCrimes, setShowCrimes] = useState(true);

  const [showHotspots, setShowHotspots] = useState(true);

  const [showCCTV, setShowCCTV] = useState(true);

  const [showRecommendations, setShowRecommendations] = useState(true);

  const [chartData, setChartData] = useState(null);

  const [aiInsights, setAIInsights] = useState(null);

  useEffect(() => {
    getDistricts()
      .then((data) => setDistricts(data))
      .catch((err) => console.error(err));
  }, []);

  useEffect(() => {
    getDashboardSummary(selectedDistrict)
      .then((data) => setSummary(data))
      .catch((err) => console.error(err));

    getDashboardCharts(selectedDistrict)
      .then((data) => setChartData(data))
      .catch((err) => console.error(err));

    getAIInsights(selectedDistrict)
      .then((data) => setAIInsights(data))
      .catch((err) => console.error(err));
  }, [selectedDistrict]);

  if (!summary) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4 }}>
      <Typography variant="h3" gutterBottom>
        AI Crime Analytics Dashboard
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4} lg={3}>
          <SummaryCard
            title="Total Crimes"
            value={summary.total_crimes}
            icon={<GavelIcon fontSize="large" color="error" />}
          />
        </Grid>

        <Grid item xs={12} md={4} lg={3}>
          <SummaryCard
            title="Total CCTV"
            value={summary.total_cctv}
            icon={<VideocamIcon fontSize="large" color="primary" />}
          />
        </Grid>

        <Grid item xs={12} md={4} lg={3}>
          <SummaryCard
            title="Hotspots"
            value={summary.total_hotspots}
            icon={<LocationOnIcon fontSize="large" color="warning" />}
          />
        </Grid>

        <Grid item xs={12} md={4} lg={3}>
          <SummaryCard
            title="Covered"
            value={summary.covered_hotspots}
            icon={<CheckCircleIcon fontSize="large" color="success" />}
          />
        </Grid>

        <Grid item xs={12} md={4} lg={3}>
          <SummaryCard
            title="Uncovered"
            value={summary.uncovered_hotspots}
            icon={<WarningAmberIcon fontSize="large" color="warning" />}
          />
        </Grid>

        <Grid item xs={12} md={4} lg={3}>
          <SummaryCard
            title="Critical CCTV"
            value={summary.critical_recommendations}
            icon={<SecurityIcon fontSize="large" color="error" />}
          />
        </Grid>
      </Grid>

      <FormControl
        sx={{
          minWidth: 260,
          mt: 4,
          mb: 2,
        }}
      >
        <InputLabel>District</InputLabel>

        <Select
          value={selectedDistrict}
          label="District"
          onChange={(e) => setSelectedDistrict(e.target.value)}
        >
          {districts.map((district) => (
            <MenuItem key={district} value={district}>
              {district}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <Box
        sx={{
          display: "flex",
          gap: 3,
          mb: 2,
        }}
      >
        <FormControlLabel
          control={
            <Checkbox
              checked={showCrimes}
              onChange={(e) => setShowCrimes(e.target.checked)}
            />
          }
          label="Show Crimes"
        />

        <FormControlLabel
          control={
            <Checkbox
              checked={showHotspots}
              onChange={(e) => setShowHotspots(e.target.checked)}
            />
          }
          label="Show Hotspots"
        />

        <FormControlLabel
            control={
                <Checkbox
                checked={showCCTV}
                onChange={(e) => setShowCCTV(e.target.checked)}
                />
            }
            label="Show CCTV"
        />

        <FormControlLabel
            control={
                <Checkbox
                checked={showRecommendations}
                onChange={(e) => setShowRecommendations(e.target.checked)}
                />
            }
            label="Show AI Recommendations"
        />

      </Box>

      <CrimeMap
        district={selectedDistrict}
        showCrimes={showCrimes}
        showHotspots={showHotspots}
        showCCTV={showCCTV}
        showRecommendations={showRecommendations}
      />

      {chartData && (
        <Grid
          container
          spacing={3}
          sx={{ mt: 2 }}
        >
          <Grid item xs={12} md={8}>
            <CrimeTypeChart
              data={chartData.crime_types}
            />
          </Grid>

          <Grid item xs={12} md={4}>
            <CrimeSeverityChart
              data={chartData.crime_severity}
            />
          </Grid>
        </Grid>
      )}

      {chartData && (
        <DistrictChart
          data={chartData}
          district={selectedDistrict}
        />
      )}

      {aiInsights && (
        <AIInsightsCard
          insights={aiInsights}
        />
      )}
    </Container>
  );
}

export default Dashboard;