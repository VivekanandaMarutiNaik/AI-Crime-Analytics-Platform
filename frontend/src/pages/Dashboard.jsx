import { useEffect, useState } from "react";

import {
  Box,
  Grid,
  Typography,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Checkbox,
  FormControlLabel,
  Autocomplete,
  TextField,
} from "@mui/material";

import GavelIcon from "@mui/icons-material/Gavel";
import VideocamIcon from "@mui/icons-material/Videocam";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import SecurityIcon from "@mui/icons-material/Security";

import DashboardLayout from "../components/layout/DashboardLayout";
import OperationalPulse from "../components/dashboard/OperationalPulse";
import AIQueryBar from "../components/ai/AIQueryBar";

import SummaryCard from "../components/SummaryCard";
import CrimeMap from "../components/CrimeMap";
import CrimeTypeChart from "../components/CrimeTypeChart";
import CrimeSeverityChart from "../components/CrimeSeverityChart";
import MonthlyTrendChart from "../components/MonthlyTrendChart";
import DistrictWiseChart from "../components/DistrictWiseChart";
import CaseStatusChart from "../components/CaseStatusChart";

import AIInsightsCard from "../components/AIInsightsCard";
import RiskScoreTable from "../components/RiskScoreTable";
import OfficerWorkloadTable from "../components/OfficerWorkloadTable";
import InvestigationPerformanceTable from "../components/InvestigationPerformanceTable";
import PredictiveTrendTable from "../components/PredictiveTrendTable";

import {
  getDashboardSummary,
  getDistricts,
  getCrimeCategory,
  getCrimeSeverity,
  getMonthlyTrend,
  getDistrictWise,
  getCaseStatus,
  getAIInsights,
  getRiskScore,
  getOfficerWorkload,
  getInvestigationPerformance,
  getPredictiveTrend,
} from "../services/api";

import "../styles/dashboard.css";

function Dashboard() {
  const [summary, setSummary] = useState(null);

  const [selectedDistrict, setSelectedDistrict] = useState("");

  const [language, setLanguage] = useState("en");

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

  const [aiInsights, setAIInsights] = useState(null);

  const [riskScore, setRiskScore] = useState(null);

  const [officerWorkload, setOfficerWorkload] = useState(null);

  const [investigationPerformance, setInvestigationPerformance] = useState(null);

   const [aiTab, setAiTab] = useState(0);

  const [predictiveTrend, setPredictiveTrend] = useState(null);
 
  const [selectedHotspot, setSelectedHotspot] = useState(null);

  useEffect(() => {
    getDistricts()
      .then((data) => setDistricts(data))
      .catch((err) => console.error(err));
  }, []);

  useEffect(() => {
    console.log("Current Language:", language);
  }, [language]);

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

    getAIInsights(selectedDistrict)
  .then((data) => setAIInsights(data))
  .catch(console.error);

    getRiskScore()
      .then((data) => setRiskScore(data))
      .catch(console.error);

    getOfficerWorkload()
      .then((data) => setOfficerWorkload(data))
      .catch(console.error);

    getInvestigationPerformance()
      .then((data) => setInvestigationPerformance(data))
      .catch(console.error);

    getPredictiveTrend(selectedDistrict)
  .then((data) => {
    setPredictiveTrend(data);
  })
  .catch((err) => {
    console.error(err);
  });
  }, [selectedDistrict]);

  if (!summary) {
    return <Typography>Loading...</Typography>;
  }

return (
<DashboardLayout
  language={language}
  setLanguage={setLanguage}
  showCrimes={showCrimes}
  setShowCrimes={setShowCrimes}
  showHotspots={showHotspots}
  setShowHotspots={setShowHotspots}
  showCCTV={showCCTV}
  setShowCCTV={setShowCCTV}
  showRecommendations={showRecommendations}
  setShowRecommendations={setShowRecommendations}
>

<Box
  sx={{
    width: "100%",
    p: 3,
    boxSizing: "border-box",
  }}
>

<AIQueryBar
  language={language}
  onIntentDetected={(intent) => {
    if (intent?.district) {
      setSelectedDistrict(intent.district);
    }
  }}
/>

<OperationalPulse />

<Typography className="section-title">
  CASE MANAGEMENT
</Typography>

<Grid
  container
  spacing={2}
  sx={{
    width: "100%",
    mb: 3,
  }}
>

  <Grid item xs={12} sm={6} md={4} lg={2}>
    <SummaryCard
      title="Total Cases"
      value={summary.total_cases}
      icon={<GavelIcon fontSize="large" />}
    />
  </Grid>

  <Grid item xs={12} sm={6} md={4} lg={2}>
    <SummaryCard
      title="Total Arrests"
      value={summary.arrests}
      icon={<VideocamIcon fontSize="large" />}
    />
  </Grid>

  <Grid item xs={12} sm={6} md={4} lg={2}>
    <SummaryCard
      title="Victims"
      value={summary.total_victims}
      icon={<LocationOnIcon fontSize="large" />}
    />
  </Grid>

  <Grid item xs={12} sm={6} md={4} lg={2}>
    <SummaryCard
      title="Accused"
      value={summary.total_accused}
      icon={<CheckCircleIcon fontSize="large" />}
    />
  </Grid>

  <Grid item xs={12} sm={6} md={4} lg={2}>
    <SummaryCard
      title="Closed Cases"
      value={summary.closed_cases}
      icon={<WarningAmberIcon fontSize="large" />}
    />
  </Grid>

  <Grid item xs={12} sm={6} md={4} lg={2}>
    <SummaryCard
      title="Charge Sheets"
      value={summary.chargesheets_filed}
      icon={<SecurityIcon fontSize="large" />}
    />
  </Grid>

</Grid>

<Box sx={{ mb: 3 }}>

<Autocomplete
  options={districts}
  value={selectedDistrict}
  onChange={(e, value) => setSelectedDistrict(value || "")}
  sx={{ width: 300 }}
  renderInput={(params) => (
    <TextField
      {...params}
      label="District"
      size="small"
    />
  )}
/>

</Box>

<Box
  sx={{
    display: "flex",
    gap: 2,
    flexWrap: "wrap",
    mb: 3,
  }}
>

<FormControlLabel
  control={
    <Checkbox
      checked={showCrimes}
      onChange={(e)=>setShowCrimes(e.target.checked)}
    />
  }
  label="Crimes"
/>

<FormControlLabel
  control={
    <Checkbox
      checked={showHotspots}
      onChange={(e)=>setShowHotspots(e.target.checked)}
    />
  }
  label="Hotspots"
/>

<FormControlLabel
  control={
    <Checkbox
      checked={showCCTV}
      onChange={(e)=>setShowCCTV(e.target.checked)}
    />
  }
  label="CCTV"
/>

<FormControlLabel
  control={
    <Checkbox
      checked={showRecommendations}
      onChange={(e)=>setShowRecommendations(e.target.checked)}
    />
  }
  label="AI CCTV"
/>

</Box>

<Typography className="section-title">
  CRIME INTELLIGENCE
</Typography>

<div className="map-section">

<div>

<CrimeMap
  district={selectedDistrict}
  showCrimes={showCrimes}
  showHotspots={showHotspots}
  showCCTV={showCCTV}
  showRecommendations={showRecommendations}
  onHotspotSelect={setSelectedHotspot}
/>

</div>

<Card className="ai-side-panel">

<div className="ai-side-tabs">

<button
className={aiTab===0 ? "active":""}
onClick={()=>setAiTab(0)}
>
Insights
</button>

<button
className={aiTab===1 ? "active":""}
onClick={()=>setAiTab(1)}
>
Risk
</button>

<button
className={aiTab===2 ? "active":""}
onClick={()=>setAiTab(2)}
>
Workload
</button>

<button
className={aiTab===3 ? "active":""}
onClick={()=>setAiTab(3)}
>
Performance
</button>

<button
className={aiTab===4 ? "active":""}
onClick={()=>setAiTab(4)}
>
Trend
</button>

</div>

<CardContent
  className="ai-side-content"
  sx={{
    flex: 1,
    overflowY: "auto",
    p: 0,
  }}
>

{aiTab===0 && aiInsights && (
<AIInsightsCard data={aiInsights}/>
)}

{aiTab===1 && riskScore && (
<RiskScoreTable data={riskScore.data}/>
)}

{aiTab===2 && officerWorkload && (
<OfficerWorkloadTable
data={officerWorkload.data}
/>
)}

{aiTab===3 && investigationPerformance && (
<InvestigationPerformanceTable
data={investigationPerformance.data}
/>
)}

{aiTab === 4 && predictiveTrend && (
  <PredictiveTrendTable
    data={predictiveTrend}
  />
)}

</CardContent>

</Card>

</div>

     <Typography className="section-title">
  CRIME ANALYTICS
</Typography>

{crimeCategory && crimeSeverity && (
  <Grid
    container
    spacing={2}
    className="analytics-grid"
  >
    <Grid item xs={12} lg={8}>
      <Card>
        <CardContent>
          <Typography
            variant="h6"
            fontWeight={600}
            gutterBottom
          >
            Crime Category Distribution
          </Typography>

          <CrimeTypeChart
            data={crimeCategory.data}
          />
        </CardContent>
      </Card>
    </Grid>

    <Grid item xs={12} lg={4}>
      <Card>
        <CardContent>
          <Typography
            variant="h6"
            fontWeight={600}
            gutterBottom
          >
            Crime Severity Distribution
          </Typography>

          <CrimeSeverityChart
            data={crimeSeverity.data}
          />
        </CardContent>
      </Card>
    </Grid>
  </Grid>
)}

<Grid
  container
  spacing={2}
  sx={{ mt: 2 }}
>

  <Grid item xs={12} lg={8}>
    <Card>
      <CardContent>

        <Typography
          variant="h6"
          fontWeight={600}
          gutterBottom
        >
          Monthly Crime Trend
        </Typography>

        {monthlyTrend && (
          <MonthlyTrendChart
            data={monthlyTrend.data}
          />
        )}

      </CardContent>
    </Card>
  </Grid>

  <Grid item xs={12} lg={4}>
    <Card>
      <CardContent>

        <Typography
          variant="h6"
          fontWeight={600}
          gutterBottom
        >
          Case Status
        </Typography>

        {caseStatus && (
          <CaseStatusChart
            data={caseStatus.data}
          />
        )}

      </CardContent>
    </Card>
  </Grid>

  <Grid item xs={12}>
    <Card>
      <CardContent>

        <Typography
          variant="h6"
          fontWeight={600}
          gutterBottom
        >
          District-wise Crime Distribution
        </Typography>

        {districtWise && (
          <DistrictWiseChart
            data={districtWise.data}
          />
        )}

      </CardContent>
    </Card>
  </Grid>

</Grid>

</Box>

</DashboardLayout>
);

}

export default Dashboard;