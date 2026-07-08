import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material";

import PsychologyIcon from "@mui/icons-material/Psychology";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import GavelIcon from "@mui/icons-material/Gavel";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import SecurityIcon from "@mui/icons-material/Security";

function AIInsightsCard({ insights }) {
  return (
    <Card sx={{ mt: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          🤖 AI Crime Insights
        </Typography>

        <List>

          <ListItem>
            <ListItemIcon>
              <LocationOnIcon color="error" />
            </ListItemIcon>

            <ListItemText
              primary={`Highest Crime District: ${insights.top_district.name}`}
              secondary={`${insights.top_district.count} reported crimes`}
            />
          </ListItem>

          <ListItem>
            <ListItemIcon>
              <GavelIcon color="primary" />
            </ListItemIcon>

            <ListItemText
              primary={`Most Common Crime: ${insights.top_crime.name}`}
              secondary={`${insights.top_crime.count} reported cases`}
            />
          </ListItem>

          <ListItem>
            <ListItemIcon>
              <PsychologyIcon color="secondary" />
            </ListItemIcon>

            <ListItemText
              primary="Crime Severity"
              secondary={`Medium: ${insights.severity_distribution.Medium}% | High: ${insights.severity_distribution.High}% | Critical: ${insights.severity_distribution.Critical}%`}
            />
          </ListItem>

          <ListItem>
            <ListItemIcon>
              <CheckCircleIcon color="success" />
            </ListItemIcon>

            <ListItemText
              primary="Covered Hotspots"
              secondary={`${insights.covered_hotspots} hotspots already protected`}
            />
          </ListItem>

          <ListItem>
            <ListItemIcon>
              <WarningAmberIcon color="warning" />
            </ListItemIcon>

            <ListItemText
              primary="Uncovered Hotspots"
              secondary={`${insights.uncovered_hotspots} hotspots still need CCTV`}
            />
          </ListItem>

          <ListItem>
            <ListItemIcon>
              <SecurityIcon color="error" />
            </ListItemIcon>

            <ListItemText
              primary="Critical Recommendation"
              secondary={`${insights.critical_recommendations} critical CCTV installation required`}
            />
          </ListItem>

        </List>
      </CardContent>
    </Card>
  );
}

export default AIInsightsCard;