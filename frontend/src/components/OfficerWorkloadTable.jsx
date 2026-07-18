import {
  Box,
  Typography,
} from "@mui/material";

function getColor(level) {
  switch (level) {
    case "High":
      return "#ef5350";

    case "Medium":
      return "#ff9800";

    default:
      return "#43a047";
  }
}

function OfficerWorkloadTable({ data }) {
  if (!data || data.length === 0) return null;
  console.log(data);

const rows = data;

  const topFive = [...data]
    .sort((a, b) => b.workload_score - a.workload_score)
    .slice(0, 5);

  return (
    <Box>

      <Typography
        sx={{
          color: "#fff",
          fontWeight: 700,
          mb: 2,
          fontSize: 15,
        }}
      >
        👮 Top Officer Workload
      </Typography>

      {topFive.map((row) => (
        <Box
          key={`${row.employee_name}-${row.district}`}
          sx={{
            bgcolor: "#1d2433",
            borderRadius: 2,
            p: 2,
            mb: 2,
            borderLeft: `4px solid ${getColor(row.workload_level)}`,
          }}
        >
          <Typography
            sx={{
              color: "#fff",
              fontWeight: 600,
              fontSize: 14,
            }}
          >
            {row.employee_name}
          </Typography>

          <Typography
            sx={{
              color: "#b8c0d4",
              fontSize: 13,
              mt: 0.5,
            }}
          >
            {row.rank}
          </Typography>

          <Typography
            sx={{
              color: "#b8c0d4",
              fontSize: 13,
            }}
          >
            {row.district}
          </Typography>

          <Typography
            sx={{
              color: "#fff",
              fontSize: 13,
              mt: 1,
            }}
          >
            Assigned Cases: {row.assigned_cases}
          </Typography>

          <Typography
            sx={{
              color: "#fff",
              fontSize: 13,
            }}
          >
            Workload: {row.workload_score}%
          </Typography>

          <Box
            sx={{
              mt: 1,
              display: "inline-block",
              px: 1.5,
              py: 0.4,
              borderRadius: 5,
              bgcolor: getColor(row.workload_level),
              color: "#fff",
              fontSize: 12,
              fontWeight: 700,
            }}
          >
            {row.workload_level}
          </Box>

        </Box>
      ))}

    </Box>
  );
}

export default OfficerWorkloadTable;