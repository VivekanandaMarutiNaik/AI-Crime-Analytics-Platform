import { useEffect, useState } from "react";  
import {
  Drawer,
  Typography,
  Box,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Stack,
} from "@mui/material";
import { getDistricts } from "../../services/api";



function FilterDrawer({ open, onClose }) {

    const [districts, setDistricts] = useState([]);

    useEffect(() => {
    async function loadDistricts() {
        try {
        const response = await getDistricts();
        setDistricts(response);
        } catch (error) {
        console.error("Failed to load districts:", error);
        }
    }

    loadDistricts();
    }, []);
  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
    >
      <Box
        sx={{
          width: 360,
          p: 3,
        }}
      >
        <Typography
          variant="h5"
          fontWeight={700}
        >
          Filters
        </Typography>

        <Typography
          variant="body2"
          color="text.secondary"
          sx={{ mb: 3 }}
        >
          Filter crime records and map layers
        </Typography>

        <Stack spacing={3}>

          <FormControl fullWidth>
            <InputLabel>District</InputLabel>

            <Select
              label="District"
              defaultValue=""
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

          <FormControl fullWidth>
            <InputLabel>Crime Type</InputLabel>

            <Select
              label="Crime Type"
              defaultValue=""
            >
              <MenuItem value="">
                All Crimes
              </MenuItem>
            </Select>
          </FormControl>

          <TextField
            label="Case ID"
            fullWidth
          />

          <Divider />

          <Button
            variant="contained"
            fullWidth
          >
            Apply Filters
          </Button>

          <Button
            variant="outlined"
            fullWidth
          >
            Reset Filters
          </Button>

        </Stack>
      </Box>
    </Drawer>
  );
}

export default FilterDrawer;