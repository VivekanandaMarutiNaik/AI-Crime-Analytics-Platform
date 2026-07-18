import { Box, Typography, Chip } from "@mui/material";

function getColor(level) {
  switch (level) {
    case "Critical":
      return "#ef4444";
    case "High":
      return "#f59e0b";
    case "Medium":
      return "#38bdf8";
    default:
      return "#22c55e";
  }
}

function RiskScoreTable({ data }) {
  if (!data) return null;

  const topFive = [...data]
    .sort((a, b) => b.risk_score - a.risk_score)
    .slice(0, 5);

  return (
    <Box>
      <Typography
        sx={{
          color: "#ffffff",
          fontWeight: 700,
          fontSize: 16,
          mb: 2,
        }}
      >
        🚨 Top 5 High Risk Districts
      </Typography>

      {topFive.map((row) => (
        <Box
          key={row.district}
          sx={{
            background: "#202838",
            border: "1px solid #2f3b52",
            borderLeft: `4px solid ${getColor(row.risk_level)}`,
            borderRadius: "14px",
            p: 2,
            mb: 2,
            transition: "0.2s",
            "&:hover": {
              borderColor: "#3b82f6",
              transform: "translateY(-2px)",
            },
          }}
        >
          <Typography
            sx={{
              color: "#ffffff",
              fontWeight: 700,
              fontSize: 15,
              mb: 1,
            }}
          >
            {row.district}
          </Typography>

          <Typography
            sx={{
              color: "#cbd5e1",
              fontSize: 13,
              mb: 1.5,
            }}
          >
            Risk Score:{" "}
            <strong>{Number(row.risk_score).toFixed(2)}</strong>
          </Typography>

          <Chip
            label={row.risk_level}
            size="small"
            sx={{
              backgroundColor: getColor(row.risk_level),
              color: "#fff",
              fontWeight: 700,
            }}
          />
        </Box>
      ))}
    </Box>
  );
}

export default RiskScoreTable;