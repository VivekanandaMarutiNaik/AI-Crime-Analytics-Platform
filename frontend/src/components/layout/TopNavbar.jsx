import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton,
  Badge,
  Avatar,
  TextField,
  InputAdornment,
  FormControl,
  Select,
  MenuItem,
  Button,
} from "@mui/material";

import NotificationsIcon from "@mui/icons-material/Notifications";
import SearchIcon from "@mui/icons-material/Search";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import FilterListIcon from "@mui/icons-material/FilterList";
import { useEffect, useState } from "react";
import { getDistricts } from "../../services/api";
function TopNavbar({
  searchText,
  setSearchText,
  onOpenFilters,
  language,
  setLanguage,
}) {


  const [districts, setDistricts] = useState([]);

    useEffect(() => {
    async function loadDistricts() {
        try {
        const data = await getDistricts();
        setDistricts(data);
        } catch (err) {
        console.error("Failed to load districts", err);
        }
    }

    loadDistricts();
    }, []);
  return (
    <AppBar
      position="static"
      elevation={0}
      sx={{
        bgcolor: "#FFFFFF",
        color: "#1E293B",
        borderBottom: "1px solid #E5E7EB",
      }}
    >
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between",
          minHeight: "72px",
        }}
      >
        {/* Left Side */}
        <Box>
          <Typography
            variant="h5"
            fontWeight={700}
          >
            AI Crime Analytics Platform
          </Typography>

          <Typography
            variant="body2"
            color="text.secondary"
          >
            Government of Karnataka • Crime Intelligence Dashboard
          </Typography>
        </Box>

        {/* Right Side */}
        <Box
          display="flex"
          alignItems="center"
          gap={2}
        >

            <FormControl size="small">
                <Select
                    defaultValue=""
                    sx={{
                        minWidth: 180,
                        bgcolor: "white",
                    }}
                    >
                    <MenuItem value="">
                        All Districts
                    </MenuItem>

                    {districts.map((district) => (
                        <MenuItem
                        key={district}
                        value={district}
                        >
                        {district}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>

            <Button
                variant="outlined"
                startIcon={<FilterListIcon />}
                onClick={onOpenFilters}
                sx={{
                    textTransform: "none",
                    height: 40,
                }}
                >
                Filters
            </Button>

          <TextField
            size="small"
            placeholder="Search Case ID, Crime Type..."
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            sx={{
                width: 300,
                bgcolor: "white",
            }}
            InputProps={{
                startAdornment: (
                <InputAdornment position="start">
                    <SearchIcon />
                </InputAdornment>
                ),
            }}
          />

          <Box
            sx={{
                display: "flex",
                border: "1px solid #D1D5DB",
                borderRadius: "20px",
                overflow: "hidden",
                height: 36,
            }}
            >
            <Button
                onClick={() => setLanguage("en")}
                sx={{
                minWidth: 60,
                borderRadius: 0,
                textTransform: "none",
                bgcolor: language === "en" ? "#1565C0" : "transparent",
                color: language === "en" ? "white" : "#374151",
                "&:hover": {
                    bgcolor: language === "en" ? "#1565C0" : "#F3F4F6",
                },
                }}
            >
                EN
            </Button>

            <Button
                onClick={() => {
                    console.log("Clicked Kannada");
                    setLanguage("kn");
                    }}
                sx={{
                minWidth: 75,
                borderRadius: 0,
                textTransform: "none",
                fontFamily: "Noto Sans Kannada, sans-serif",
                bgcolor: language === "kn" ? "#1565C0" : "transparent",
                color: language === "kn" ? "white" : "#374151",
                "&:hover": {
                    bgcolor: language === "kn" ? "#1565C0" : "#F3F4F6",
                },
                }}
            >
                ಕನ್ನಡ
            </Button>
            </Box>

          <IconButton>
            <Badge
              badgeContent={3}
              color="error"
            >
                
              <NotificationsIcon />
            </Badge>
          </IconButton>

          <Avatar
            sx={{
              bgcolor: "#1565C0",
            }}
          >
            <AccountCircleIcon />
          </Avatar>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default TopNavbar;