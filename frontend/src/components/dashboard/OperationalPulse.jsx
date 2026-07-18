import { Grid, Card, CardContent, Typography, Box } from "@mui/material";

import CalendarTodayIcon from "@mui/icons-material/CalendarToday";
import AssignmentIcon from "@mui/icons-material/Assignment";
import LocalFireDepartmentIcon from "@mui/icons-material/LocalFireDepartment";
import VideocamIcon from "@mui/icons-material/Videocam";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";

const items = [
  {
    title: "Today's Cases",
    value: 47,
    icon: <CalendarTodayIcon color="primary" />,
  },
  {
    title: "Active Investigations",
    value: 126,
    icon: <AssignmentIcon color="primary" />,
  },
  {
    title: "High Risk Areas",
    value: 9,
    icon: <LocalFireDepartmentIcon color="error" />,
  },
  {
    title: "CCTV Coverage",
    value: "68%",
    icon: <VideocamIcon color="success" />,
  },
  {
    title: "AI Alerts",
    value: 5,
    icon: <AutoAwesomeIcon color="warning" />,
  },
];

function OperationalPulse() {
  return (
    <Box sx={{ mb: 3 }}>
      <Typography
        variant="overline"
        sx={{
          fontWeight: 700,
          color: "text.secondary",
          letterSpacing: 1,
        }}
      >
        OPERATIONAL PULSE
      </Typography>

      <Grid container spacing={2} sx={{ mt: 0.5 }}>
        {items.map((item) => (
          <Grid item xs={12} sm={6} md={2.4} key={item.title}>
            <Card
              sx={{
                borderRadius: 3,
                height: "100%",
              }}
            >
              <CardContent>
                {item.icon}

                <Typography
                  variant="h5"
                  fontWeight={700}
                  sx={{ mt: 1 }}
                >
                  {item.value}
                </Typography>

                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  {item.title}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default OperationalPulse;