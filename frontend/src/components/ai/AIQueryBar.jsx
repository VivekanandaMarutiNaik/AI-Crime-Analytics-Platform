import { useState } from "react";

import {
  Paper,
  TextField,
  IconButton,
  Stack,
  Typography,
  CircularProgress,
  Chip,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import MicIcon from "@mui/icons-material/Mic";

import { askAI } from "../../services/api";

function AIQueryBar({
  language,
  onIntentDetected,
}) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const startListening = () => {

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert("Speech recognition is not supported in this browser.");
    return;
  }

  const recognition = new SpeechRecognition();

  recognition.lang = language === "kn" ? "kn-IN" : "en-IN";

  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    setQuery(transcript);
  };

  recognition.onerror = (event) => {
    console.error("Speech Recognition Error:", event.error);
  };

  recognition.start();
};

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      setLoading(true);
      console.log("Language sent to backend:", language);
      const data = await askAI(query, language);

      console.log("AI Response:", data);

      setResult(data);

      if (onIntentDetected) {
        onIntentDetected(data.intent);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper
      elevation={0}
      sx={{
        p: 2,
        mb: 2,
        borderRadius: 3,
        backgroundColor: "#141924",
        border: "1px solid #242B3B",
      }}
    >
      <Typography
        variant="subtitle2"
        sx={{
          color: "#8891A5",
          mb: 1,
          fontWeight: 600,
        }}
      >
        {language === "kn" ? "ಎಐ ಅನ್ನು ಕೇಳಿ" : "Ask AI"}
      </Typography>

      <Stack direction="row" spacing={1}>
        <TextField
          fullWidth
          size="small"
          placeholder={
            language === "kn"
                ? "ಅಪರಾಧಗಳ ಬಗ್ಗೆ ಕೇಳಿ..."
                : "Ask AI about crimes..."
            }
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSearch();
            }
          }}
          sx={{
            "& .MuiOutlinedInput-root": {
              borderRadius: 2,
              backgroundColor: "#1B2130",
              color: "#fff",

              "& fieldset": {
                borderColor: "#2A3142",
              },

              "&:hover fieldset": {
                borderColor: "#2E7DE0",
              },

              "&.Mui-focused fieldset": {
                borderColor: "#2E7DE0",
              },
            },

            input: {
              color: "#fff",
            },
          }}
        />

        <IconButton
          onClick={handleSearch}
          disabled={loading}
          sx={{
            bgcolor: "#2E7DE0",
            color: "#fff",
            "&:hover": {
              bgcolor: "#2568C9",
            },
          }}
        >
          {loading ? (
            <CircularProgress size={22} sx={{ color: "white" }} />
          ) : (
            <SearchIcon />
          )}
        </IconButton>

        <IconButton
  onClick={startListening}
  sx={{
    bgcolor: "#1B2130",
    color: "#fff",
    border: "1px solid #2A3142",
  }}
>
  <MicIcon />
</IconButton>
      </Stack>

      {result && (
        <Paper
          sx={{
            mt: 2,
            p: 2,
            background: "#1B2130",
            borderRadius: 2,
          }}
        >
          <Typography color="white" fontWeight={600}>
            AI Understanding
          </Typography>

          {result.answer ? (
            <Typography
                color="#4CAF50"
                mt={1}
                fontWeight={600}
                sx={{
                    whiteSpace: "pre-line",
                    textAlign: "left",
                    lineHeight: 1.8,
                }}
                >
                {result.answer}
                </Typography>
            ) : (
            <Typography 
            color="#9CA3AF" mt={1}>
                {result.translated_text}
            </Typography>
            )}

          <Stack direction="row" spacing={1} mt={2} flexWrap="wrap">
            {result.intent?.district && (
                <Chip
                label={`District: ${result.intent.district}`}
                color="primary"
                size="small"
                />
            )}

            {result.intent?.crime_type && (
                <Chip
                label={`Crime: ${result.intent.crime_type}`}
                color="success"
                size="small"
                />
            )}

            {result.intent?.intent && (
                <Chip
                label={`Intent: ${result.intent.intent}`}
                color="warning"
                size="small"
                />
            )}
            </Stack>
        </Paper>
      )}

            <Typography
        sx={{
          mt: 2,
          color: "#8891A5",
          fontSize: 13,
        }}
      >
        {language === "kn" ? "ಉದಾಹರಣೆ:" : "Example:"}
      </Typography>

      <Typography
        sx={{
          color: "#E6E9F0",
          fontSize: 13,
        }}
      >
        {language === "kn"
          ? "ಮೈಸೂರಿನಲ್ಲಿ ಕಳ್ಳತನ ಪ್ರಕರಣಗಳನ್ನು ತೋರಿಸಿ"
          : "Show theft cases in Mysuru"}
      </Typography>

      <Typography
        sx={{
          color: "#8891A5",
          fontSize: 12,
          mt: 0.5,
        }}
      >
        {language === "kn" ? "ಅಥವಾ" : "or"}
      </Typography>

      <Typography
        sx={{
          color: "#E6E9F0",
          fontSize: 13,
        }}
      >
        {language === "kn"
          ? "Show theft cases in Mysuru"
          : "ಮೈಸೂರಿನಲ್ಲಿ ಕಳ್ಳತನ ಪ್ರಕರಣಗಳನ್ನು ತೋರಿಸಿ"}
      </Typography>
    </Paper>
  );
}

export default AIQueryBar;