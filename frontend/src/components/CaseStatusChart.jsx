import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";

import {
  Card,
  CardContent,
  Typography,
} from "@mui/material";

const COLORS = [
  "#2e7d32",
  "#1976d2",
  "#d32f2f",
  "#ff9800",
];

function CaseStatusChart({ data }) {
  return (
    <Card sx={{ mt: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Case Status Distribution
        </Typography>

        <ResponsiveContainer width="100%" height={350}>
          <PieChart>
            <Pie
              data={data}
              dataKey="count"
              nameKey="label"
              outerRadius={120}
            >
              {data.map((entry, index) => (
                <Cell
                  key={entry.label}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>

            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export default CaseStatusChart;