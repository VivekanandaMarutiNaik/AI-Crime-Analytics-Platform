import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

import {
  Card,
  CardContent,
  Typography,
} from "@mui/material";

function CrimeTypeChart({ data }) {
  return (
    <Card sx={{ mt: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Crime Type Distribution
        </Typography>

        <ResponsiveContainer width="100%" height={450}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="crime_type"
              angle={-45}
              textAnchor="end"
              interval={0}
              height={120}
            />

            <YAxis />

            <Tooltip />

            <Bar
              dataKey="count"
              fill="#1976d2"
            />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export default CrimeTypeChart;