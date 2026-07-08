import { Card, CardContent, Typography } from "@mui/material";
import Box from "@mui/material/Box";



function SummaryCard({ title, value, icon }) {
  return (
    <Card
      sx={{
        minWidth: 250,
        borderRadius: 3,
        boxShadow: 3,
        transition: "0.3s",
        "&:hover": {
          transform: "translateY(-5px)",
          boxShadow: 6,
        },
      }}
    >
        <CardContent>
            <Box
                sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                }}
            >
                <Box>
                <Typography
                    variant="h6"
                    color="text.secondary"
                >
                    {title}
                </Typography>

                <Typography
                    variant="h3"
                    fontWeight="bold"
                >
                    {value}
                </Typography>
                </Box>

                {icon}
            </Box>
        </CardContent>
    </Card>
  );
}

export default SummaryCard;