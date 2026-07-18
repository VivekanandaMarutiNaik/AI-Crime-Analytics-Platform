import {
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Box,
} from "@mui/material";

import LocationOnIcon from "@mui/icons-material/LocationOn";
import GavelIcon from "@mui/icons-material/Gavel";
import SecurityIcon from "@mui/icons-material/Security";
import PsychologyIcon from "@mui/icons-material/Psychology";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";

function AIInsightsCard({ data }) {
  if (!data) return null;

  return (
    <Box>
      <List disablePadding>

        <ListItem>
          <ListItemIcon>
            <LocationOnIcon color="error" />
          </ListItemIcon>

          <ListItemText
            primary="Highest Crime District"
            secondary={`${data.highest_crime_district?.district} (${data.highest_crime_district?.cases} cases)`}
            primaryTypographyProps={{
              sx: {
                color: "#ffffff",
                fontWeight: 600,
                fontSize: 16,
              },
            }}
            secondaryTypographyProps={{
              sx: {
                color: "#cbd5e1",
                fontSize: 14,
              },
            }}
          />
        </ListItem>

        <Divider sx={{ borderColor: "#2d3748" }} />

        <ListItem>
          <ListItemIcon>
            <GavelIcon color="primary" />
          </ListItemIcon>

          <ListItemText
            primary="Highest Crime Category"
            secondary={`${data.highest_crime_category?.category} (${data.highest_crime_category?.cases} cases)`}
            primaryTypographyProps={{
              sx: {
                color: "#ffffff",
                fontWeight: 600,
                fontSize: 16,
              },
            }}
            secondaryTypographyProps={{
              sx: {
                color: "#cbd5e1",
                fontSize: 14,
              },
            }}
          />
        </ListItem>

        <Divider sx={{ borderColor: "#2d3748" }} />

        <ListItem>
          <ListItemIcon>
            <SecurityIcon color="error" />
          </ListItemIcon>

          <ListItemText
            primary="Most Dangerous Taluk"
            secondary={`${data.most_dangerous_taluk?.taluk} (${data.most_dangerous_taluk?.cases} cases)`}
            primaryTypographyProps={{
              sx: {
                color: "#ffffff",
                fontWeight: 600,
                fontSize: 16,
              },
            }}
            secondaryTypographyProps={{
              sx: {
                color: "#cbd5e1",
                fontSize: 14,
              },
            }}
          />
        </ListItem>

        <Divider sx={{ borderColor: "#2d3748" }} />

        <ListItem>
          <ListItemIcon>
            <PsychologyIcon color="secondary" />
          </ListItemIcon>

          <ListItemText
            primary="Peak Crime Time"
            secondary={data.peak_crime_time}
            primaryTypographyProps={{
              sx: {
                color: "#ffffff",
                fontWeight: 600,
                fontSize: 16,
              },
            }}
            secondaryTypographyProps={{
              sx: {
                color: "#cbd5e1",
                fontSize: 14,
              },
            }}
          />
        </ListItem>

        <Divider sx={{ borderColor: "#2d3748" }} />

        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="success" />
          </ListItemIcon>

          <ListItemText
            primary="Arrest Rate"
            secondary={`${data.arrest_rate}%`}
            primaryTypographyProps={{
              sx: {
                color: "#ffffff",
                fontWeight: 600,
                fontSize: 16,
              },
            }}
            secondaryTypographyProps={{
              sx: {
                color: "#cbd5e1",
                fontSize: 14,
              },
            }}
          />
        </ListItem>

        <Divider sx={{ borderColor: "#2d3748" }} />

        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="primary" />
          </ListItemIcon>

          <ListItemText
            primary="Chargesheet Rate"
            secondary={`${data.chargesheet_rate}%`}
            primaryTypographyProps={{
              sx: {
                color: "#ffffff",
                fontWeight: 600,
                fontSize: 16,
              },
            }}
            secondaryTypographyProps={{
              sx: {
                color: "#cbd5e1",
                fontSize: 14,
              },
            }}
          />
        </ListItem>

        <Divider sx={{ borderColor: "#2d3748" }} />

        <ListItem>
          <ListItemIcon>
            <PsychologyIcon color="primary" />
          </ListItemIcon>

          <ListItemText
            primary="Fastest Growing Category"
            secondary={data.fastest_growing_category}
            primaryTypographyProps={{
              sx: {
                color: "#ffffff",
                fontWeight: 600,
                fontSize: 16,
              },
            }}
            secondaryTypographyProps={{
              sx: {
                color: "#cbd5e1",
                fontSize: 14,
              },
            }}
          />
        </ListItem>

        <Divider sx={{ borderColor: "#2d3748" }} />

        <ListItem>
          <ListItemIcon>
            <SecurityIcon color="success" />
          </ListItemIcon>

          <ListItemText
            primary="CCTV Coverage"
            secondary={`${data.cctv_coverage}%`}
            primaryTypographyProps={{
              sx: {
                color: "#ffffff",
                fontWeight: 600,
                fontSize: 16,
              },
            }}
            secondaryTypographyProps={{
              sx: {
                color: "#cbd5e1",
                fontSize: 14,
              },
            }}
          />
        </ListItem>

      </List>
    </Box>
  );
}

export default AIInsightsCard;