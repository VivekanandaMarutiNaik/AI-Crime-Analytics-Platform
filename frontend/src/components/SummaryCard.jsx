import { Card, CardContent, Typography, Box, Avatar } from "@mui/material";

function SummaryCard({ title, value, icon }) {
  return (
    <Card
      sx={{
        height: "100%",
        borderRadius: 4,
        boxShadow: "0 8px 24px rgba(0,0,0,0.08)",
        transition: "all 0.3s ease",
        border: "1px solid #E8EDF3",
        "&:hover": {
          transform: "translateY(-6px)",
          boxShadow: "0 14px 30px rgba(21,101,192,0.18)",
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box
          display="flex"
          justifyContent="space-between"
          alignItems="center"
        >
          <Box>
            <Typography
              variant="body2"
              sx={{
                color: "text.secondary",
                fontWeight: 600,
                letterSpacing: 0.5,
                textTransform: "uppercase",
                mb: 1,
              }}
            >
              {title}
            </Typography>

            <Typography
              variant="h4"
              sx={{
                fontWeight: 700,
                color: "#1A237E",
              }}
            >
              {Number(value).toLocaleString()}
            </Typography>
          </Box>

          <Avatar
            sx={{
              width: 64,
              height: 64,
              bgcolor: "rgba(21,101,192,0.12)",
              color: "#1565C0",
            }}
          >
            {icon}
          </Avatar>
        </Box>
      </CardContent>
    </Card>
  );
}

export default SummaryCard;