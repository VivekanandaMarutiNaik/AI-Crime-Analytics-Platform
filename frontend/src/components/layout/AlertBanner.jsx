import { Alert, Button } from "@mui/material";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";

function AlertBanner() {
  return (
    <Alert
      severity="error"
      icon={<WarningAmberIcon />}
      action={
        <Button color="inherit" size="small" variant="outlined">
          View Details
        </Button>
      }
      sx={{
        borderRadius: 0,
        fontWeight: 600,
      }}
    >
      Critical Alert: Unusual crime spike detected in Whitefield sub-division —
      3 incidents reported in the last 4 hours.
    </Alert>
  );
}

export default AlertBanner;