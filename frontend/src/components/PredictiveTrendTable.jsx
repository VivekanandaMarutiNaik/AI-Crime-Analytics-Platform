import { Box, Typography, Chip, LinearProgress } from "@mui/material";
import LightbulbIcon from "@mui/icons-material/Lightbulb";

function getColor(trend) {
  if (trend === "Increasing") return "#ef5350";
  if (trend === "Stable") return "#ff9800";
  return "#4caf50";
}

function PredictiveTrendTable({ data }) {
  if (!data || data.length === 0) return null;

 const topFive = [...data]
  .sort((a, b) => b.growth_percentage - a.growth_percentage)
  .slice(0, 5);

const getRecommendation = (trend) => {
  if (trend === "Increasing") {
    return "Increase patrols & CCTV monitoring";
  }

  if (trend === "Stable") {
    return "Maintain current police deployment";
  }

  return "Continue routine surveillance";
};

  return (
    <Box>
      <Typography
        sx={{
          color: "#fff",
          fontWeight: 700,
          fontSize: 18,
          mb: 2,
        }}
      >
        🔮 AI Crime Prediction
      </Typography>

      {topFive.map((row) => (
        <Box
  key={row.district}
  sx={{
    bgcolor: "#232b3b",
    borderRadius: 2,
    p: 1.5,
    mb: 1.5,
    borderLeft: `4px solid ${getColor(row.trend)}`,
  }}
>
  <Typography
    sx={{
      color: "#fff",
      fontWeight: 700,
      fontSize: 15,
      mb: 0.5,
    }}
  >
    {row.district}
  </Typography>

  <Box
  sx={{
    display: "flex",
    justifyContent: "space-between",
    mt: 1,
    mb: 1,
  }}
>
  <Typography
    sx={{
      color: "#cbd5e1",
      fontSize: 13,
    }}
  >
    Current: <b>{row.current_month_cases}</b>
  </Typography>

  <Typography
    sx={{
      color: "#cbd5e1",
      fontSize: 13,
    }}
  >
    Next: <b>{row.predicted_next_month_cases}</b>
  </Typography>
</Box>

<Typography
  sx={{
    color:
      row.predicted_next_month_cases > row.current_month_cases
        ? "#ef5350"
        : row.predicted_next_month_cases < row.current_month_cases
        ? "#4caf50"
        : "#ff9800",
    fontSize: 12,
    fontWeight: 600,
    mt: 0.5,
  }}
>
  {row.predicted_next_month_cases > row.current_month_cases
    ? `▲ Expected Increase: +${
        row.predicted_next_month_cases - row.current_month_cases
      } cases`
    : row.predicted_next_month_cases < row.current_month_cases
    ? `▼ Expected Decrease: ${
        row.current_month_cases - row.predicted_next_month_cases
      } cases`
    : "■ No change expected"}
</Typography>
  <Typography
  sx={{
    color: "#cbd5e1",
    fontSize: 13,
    mt: 0.5,
  }}
>
  Confidence: <b>{row.confidence}%</b>
</Typography>

<LinearProgress
  variant="determinate"
  value={row.confidence}
  sx={{
    mt: 0.5,
    height: 6,
    borderRadius: 3,
    bgcolor: "#1e293b",
    "& .MuiLinearProgress-bar": {
      bgcolor: getColor(row.trend),
    },
  }}
/>

<Chip
  size="small"
  label={`${row.trend} (${row.growth_percentage}%)`}
  sx={{
    mt: 1,
    bgcolor: getColor(row.trend),
    color: "#fff",
    fontWeight: 700,
  }}
/>

<Box
  sx={{
    display: "flex",
    alignItems: "center",
    gap: 0.5,
    mt: 1,
  }}
>
  <LightbulbIcon
  sx={{
    color: getColor(row.trend),
    fontSize: 16,
  }}
/>

 <Typography
  sx={{
    color: getColor(row.trend),
    fontSize: 12,
    fontStyle: "italic",
    fontWeight: 500,
  }}
>
  {getRecommendation(row.trend)}
</Typography>
</Box>

</Box>
        
      ))}
    </Box>
  );
}

export default PredictiveTrendTable;