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
  "#1976d2",
  "#ff9800",
  "#d32f2f",
  "#7b1fa2",
];

function CrimeSeverityChart({ data }) {
  return (
    <Card sx={{ mt: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Crime Severity Distribution
        </Typography>

        <ResponsiveContainer width="100%" height={450}>
          <PieChart>
            <Pie
                data={data}
                dataKey="count"
                nameKey="severity"
                cx="50%"
                cy="50%"
                outerRadius={140}
                label={false}
            >
              {data.map((entry, index) => (
                <Cell
                  key={entry.severity}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>

            <Tooltip
                formatter={(value, name, props) => {
                    const total = data.reduce((sum, item) => sum + item.count, 0);
                    const percent = ((props.payload.count / total) * 100).toFixed(1);

                    return [`${value} (${percent}%)`, name];
                }}
            />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export default CrimeSeverityChart;