import {
  Box,
  Typography,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Switch,
} from "@mui/material";

import DashboardIcon from "@mui/icons-material/Dashboard";
import LocalPoliceIcon from "@mui/icons-material/LocalPolice";
import VideocamIcon from "@mui/icons-material/Videocam";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import ApartmentIcon from "@mui/icons-material/Apartment";
import LocalHospitalIcon from "@mui/icons-material/LocalHospital";
import SchoolIcon from "@mui/icons-material/School";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import DirectionsBusIcon from "@mui/icons-material/DirectionsBus";
import TrainIcon from "@mui/icons-material/Train";

function Sidebar({
  showCrimes,
  setShowCrimes,
  showHotspots,
  setShowHotspots,
  showCCTV,
  setShowCCTV,
  showRecommendations,
  setShowRecommendations,
}) {
  return (
    <Box
      sx={{
        width: 250,
        bgcolor: "#141924",
        color: "white",
        height: "100vh",
        borderRight: "1px solid #252C3D",
        overflowY: "auto",
        flexShrink: 0,
      }}
    >
      <Typography
        sx={{
          p: 2,
          fontWeight: 700,
          fontSize: 14,
          letterSpacing: 1,
          color: "#8F98AE",
        }}
      >
        CRIME LAYERS
      </Typography>

      <List dense>

        <ListItemButton>
          <ListItemIcon>
            <DashboardIcon sx={{ color: "#F04438" }} />
          </ListItemIcon>

          <ListItemText primary="Crimes" />

          <Switch
            checked={showCrimes}
            onChange={(e) => setShowCrimes(e.target.checked)}
          />
        </ListItemButton>

        <ListItemButton>
          <ListItemIcon>
            <LocationOnIcon sx={{ color: "#F79009" }} />
          </ListItemIcon>

          <ListItemText primary="Hotspots" />

          <Switch
            checked={showHotspots}
            onChange={(e) => setShowHotspots(e.target.checked)}
          />
        </ListItemButton>

        <ListItemButton>
          <ListItemIcon>
            <VideocamIcon sx={{ color: "#2E7DE0" }} />
          </ListItemIcon>

          <ListItemText primary="Existing CCTV" />

          <Switch
            checked={showCCTV}
            onChange={(e) => setShowCCTV(e.target.checked)}
          />
        </ListItemButton>

        <ListItemButton>
          <ListItemIcon>
            <AutoAwesomeIcon sx={{ color: "#12B76A" }} />
          </ListItemIcon>

          <ListItemText primary="AI Recommended CCTV" />

          <Switch
            checked={showRecommendations}
            onChange={(e) =>
              setShowRecommendations(e.target.checked)
            }
          />
        </ListItemButton>

        <ListItemButton>
          <ListItemIcon>
            <LocalPoliceIcon sx={{ color: "#9B6EF3" }} />
          </ListItemIcon>

          <ListItemText primary="Police Stations" />

          <Switch />
        </ListItemButton>

      </List>

      <Divider sx={{ bgcolor: "#252C3D", my: 2 }} />

      <Typography
        sx={{
          px: 2,
          pb: 1,
          fontWeight: 700,
          fontSize: 14,
          color: "#8F98AE",
        }}
      >
        POINTS OF INTEREST
      </Typography>

      <List dense>

        <ListItemButton>
          <ListItemIcon>
            <LocalHospitalIcon sx={{ color: "#B0B8C9" }} />
          </ListItemIcon>

          <ListItemText primary="Hospitals" />

          <Switch />
        </ListItemButton>

        <ListItemButton>
          <ListItemIcon>
            <SchoolIcon sx={{ color: "#B0B8C9" }} />
          </ListItemIcon>

          <ListItemText primary="Schools" />

          <Switch />
        </ListItemButton>

        <ListItemButton>
          <ListItemIcon>
            <AccountBalanceIcon sx={{ color: "#B0B8C9" }} />
          </ListItemIcon>

          <ListItemText primary="Banks" />

          <Switch />
        </ListItemButton>

        <ListItemButton>
          <ListItemIcon>
            <DirectionsBusIcon sx={{ color: "#B0B8C9" }} />
          </ListItemIcon>

          <ListItemText primary="Bus Stands" />

          <Switch />
        </ListItemButton>

        <ListItemButton>
          <ListItemIcon>
            <TrainIcon sx={{ color: "#B0B8C9" }} />
          </ListItemIcon>

          <ListItemText primary="Railway Stations" />

          <Switch />
        </ListItemButton>

      </List>

      <Divider sx={{ bgcolor: "#252C3D", my: 2 }} />

      <List dense>

        <ListItemButton>
          <ListItemIcon>
            <ApartmentIcon sx={{ color: "#2E7DE0" }} />
          </ListItemIcon>

          <ListItemText primary="Analytics" />
        </ListItemButton>

      </List>
    </Box>
  );
}

export default Sidebar;