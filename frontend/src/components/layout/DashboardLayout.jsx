import { Box } from "@mui/material";
import { useState } from "react";
import Sidebar from "./Sidebar";
import TopNavbar from "./TopNavbar";
import AlertBanner from "./AlertBanner";
import FilterDrawer from "./FilterDrawer";

function DashboardLayout({

  
  children,
  language,
  setLanguage,
  showCrimes,
  setShowCrimes,
  showHotspots,
  setShowHotspots,
  showCCTV,
  setShowCCTV,
  showRecommendations,
  setShowRecommendations,
}) {

  const [searchText, setSearchText] = useState("");
  const [filterOpen, setFilterOpen] = useState(false);
  return (
    <Box
      sx={{
        display: "flex",
        minHeight: "100vh",
        bgcolor: "#F5F7FA",
      }}
    >
      <Sidebar
        showCrimes={showCrimes}
        setShowCrimes={setShowCrimes}
        showHotspots={showHotspots}
        setShowHotspots={setShowHotspots}
        showCCTV={showCCTV}
        setShowCCTV={setShowCCTV}
        showRecommendations={showRecommendations}
        setShowRecommendations={setShowRecommendations}
      />

      <Box
        sx={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
        }}
      >
        <>
            <AlertBanner />

            <TopNavbar
                searchText={searchText}
                setSearchText={setSearchText}
                onOpenFilters={() => setFilterOpen(true)}
                language={language}
                setLanguage={setLanguage}
            />

            <FilterDrawer
                open={filterOpen}
                onClose={() => setFilterOpen(false)}
            />
        </>

<Box
  sx={{
    flex: 1,
    width: "100%",
    maxWidth: "100%",
    px: 3,
    py: 2,
    overflowY: "auto",
  }}
>
          {children}
        </Box>
      </Box>
    </Box>
  );
}

export default DashboardLayout;