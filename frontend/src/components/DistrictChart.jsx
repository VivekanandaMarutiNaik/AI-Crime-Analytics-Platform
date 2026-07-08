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

function DistrictChart({ data, district }) {
  const chartData =
    district && data.police_station_distribution
        ? data.police_station_distribution
        : data.district_distribution;

  const title = district
    ? `Top Police Stations in ${district}`
    : "Top 10 Districts by Crime Count";

  const yAxisKey = district
    ? "police_station"
    : "district";

  return (
    <Card sx={{ mt: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
            {title}
        </Typography>

        <ResponsiveContainer width="100%" height={450}>
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{
              top: 10,
              right: 30,
              left: 40,
              bottom: 10,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis type="number" />

            <YAxis
                dataKey={yAxisKey}
                type="category"
                width={180}
            />
            <Tooltip
                formatter={(value) => [`${value} Crimes`, "Reported Cases"]}
            />

            <Bar
              dataKey="count"
              fill="#7b1fa2"
            />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export default DistrictChart;