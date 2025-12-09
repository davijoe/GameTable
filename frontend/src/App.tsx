import "./App.css";
import { Box } from "@chakra-ui/react";
import GamesTab from "./components/tabs/Games";
import WeatherTab from "./components/tabs/WeatherTab";
import ProfileTab from "./components/tabs/Profile";
import Header from "./components/Header";
import { AuthProvider } from "./context/AuthContext";

import { Route, Routes } from "react-router-dom";
import SelectedGame from "./components/game/SelectedGame";

const HEADER_HEIGHT = "80px"

function App() {
  return (
    <AuthProvider>
      <Header height={HEADER_HEIGHT} />
      <Box pt={`${HEADER_HEIGHT}`}></Box>
      <Box p="2%">
        <Routes>
          <Route path="/games" element={<GamesTab />} />
          <Route path="/games/:gameId" element={<SelectedGame />} />
          <Route path="/weather" element={<WeatherTab />} />
          <Route path="/profile" element={<ProfileTab />} />
          <Route path="*" element={<GamesTab />} /> {/* should maybe be error page instead? */}
        </Routes>
      </Box>
    </AuthProvider>
  );
}

export default App;
