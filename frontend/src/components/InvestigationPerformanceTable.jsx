import {
  Box,
  Typography,
  LinearProgress,
} from "@mui/material";

function getColor(rate) {
  if (rate >= 80) return "#43a047";
  if (rate >= 60) return "#ff9800";
  return "#ef5350";
}

function InvestigationPerformanceTable({ data }) {
  if (!data || data.length === 0) return null;

  const topFive = [...data]
    .sort((a, b) => b.performance_score - a.performance_score)
    .slice(0, 5);

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
        📈 Investigation Performance
      </Typography>

      {topFive.map((row) => (
        <Box
          key={row.district}
          sx={{
            bgcolor: "#232b3b",
            borderRadius: 2,
            p: 2,
            mb: 2,
            borderLeft: `4px solid ${getColor(row.performance_score)}`,
          }}
        >
          <Typography
            sx={{
              color: "#fff",
              fontWeight: 700,
              fontSize: 16,
            }}
          >
            {row.district}
          </Typography>

          <Typography
            sx={{
              color: "#cbd5e1",
              fontSize: 13,
              mt: 1,
            }}
          >
            Performance Score: <b>{row.performance_score}%</b>
          </Typography>

          <LinearProgress
            variant="determinate"
            value={row.performance_score}
            sx={{
              mt: 1,
              height: 6,
              borderRadius: 3,
              bgcolor: "#1b2230",
              "& .MuiLinearProgress-bar": {
                bgcolor: getColor(row.performance_score),
              },
            }}
          />

          <Typography
            sx={{
              color: "#94a3b8",
              fontSize: 12,
              mt: 1,
              fontStyle: "italic",
            }}
          >
            {row.performance_score >= 80
              ? "Excellent investigation efficiency"
              : row.performance_score >= 60
              ? "Average investigation efficiency"
              : "Needs investigation improvement"}
          </Typography>

        </Box>
      ))}

    </Box>
  );
}

export default InvestigationPerformanceTable;