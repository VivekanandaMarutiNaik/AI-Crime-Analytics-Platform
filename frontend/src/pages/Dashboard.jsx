import { useEffect, useState } from "react";
import {
  getDashboardSummary,
  getDistricts,
  getCrimeCategory,
  getCrimeSeverity,
  getMonthlyTrend,
  getDistrictWise,
  getCaseStatus,
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
import MonthlyTrendChart from "../components/MonthlyTrendChart";
import DistrictWiseChart from "../components/DistrictWiseChart";
import CaseStatusChart from "../components/CaseStatusChart";

function Dashboard() {
  const [summary, setSummary] = useState(null);

  const [selectedDistrict, setSelectedDistrict] = useState("");

  const [districts, setDistricts] = useState([]);

  const [showCrimes, setShowCrimes] = useState(true);

  const [showHotspots, setShowHotspots] = useState(true);

  const [showCCTV, setShowCCTV] = useState(true);

  const [showRecommendations, setShowRecommendations] = useState(true);

  const [crimeCategory, setCrimeCategory] = useState(null);

  const [crimeSeverity, setCrimeSeverity] = useState(null);

  const [monthlyTrend, setMonthlyTrend] = useState(null);

  const [districtWise, setDistrictWise] = useState(null);

  const [caseStatus, setCaseStatus] = useState(null);

  useEffect(() => {
    getDistricts()
      .then((data) => setDistricts(data))
      .catch((err) => console.error(err));
  }, []);

  useEffect(() => {
    getDashboardSummary(selectedDistrict)
      .then((data) => setSummary(data))
      .catch((err) => console.error(err));

    getCrimeCategory(selectedDistrict)
      .then((data) => setCrimeCategory(data))
      .catch(console.error);

    getCrimeSeverity(selectedDistrict)
      .then((data) => setCrimeSeverity(data))
      .catch(console.error);

    getMonthlyTrend(selectedDistrict)
      .then((data) => setMonthlyTrend(data))
      .catch(console.error);

    getDistrictWise()
      .then((data) => setDistrictWise(data))
      .catch(console.error);

    getCaseStatus(selectedDistrict)
      .then((data) => setCaseStatus(data))
      .catch(console.error);
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
            title="Total Cases"
            value={summary.total_cases}
            icon={<GavelIcon fontSize="large" color="error" />}
          />
        </Grid>

        <Grid item xs={12} md={4} lg={3}>
          <SummaryCard
            title="Total Arrests"
            value={summary.arrests}
            icon={<VideocamIcon fontSize="large" color="primary" />}
          />
        </Grid>

        <Grid item xs={12} md={4} lg={3}>
          <SummaryCard
            title="Victims"
            value={summary.total_victims}
            icon={<LocationOnIcon fontSize="large" color="warning" />}
          />
        </Grid>

        <Grid item xs={12} md={4} lg={3}>
          <SummaryCard
            title="Accused"
            value={summary.total_accused}
            icon={<CheckCircleIcon fontSize="large" color="success" />}
          />
        </Grid>

        <Grid item xs={12} md={4} lg={3}>
          <SummaryCard
            title="Closed Cases"
            value={summary.closed_cases}
            icon={<WarningAmberIcon fontSize="large" color="warning" />}
          />
        </Grid>

        <Grid item xs={12} md={4} lg={3}>
          <SummaryCard
            title="Charge Sheets Filed"
            value={summary.chargesheets_filed}
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

      {crimeCategory && crimeSeverity && (
        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid item xs={12} md={8}>
            <CrimeTypeChart
              data={crimeCategory.data}
            />
          </Grid>

          <Grid item xs={12} md={4}>
            <CrimeSeverityChart
              data={crimeSeverity.data}
            />
          </Grid>
        </Grid>
      )}

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={8}>
          {monthlyTrend && (
            <MonthlyTrendChart data={monthlyTrend.data} />
          )}
        </Grid>

        <Grid item xs={12} md={4}>
          {caseStatus && (
            <CaseStatusChart data={caseStatus.data} />
          )}
        </Grid>

        <Grid item xs={12}>
          {districtWise && (
            <DistrictWiseChart data={districtWise.data} />
          )}
  </Grid>
</Grid>
      
    </Container>
  );
}

export default Dashboard;