import "./App.css";
import { Box } from "@chakra-ui/react";
import GamesTab from "./components/tabs/Games";
import FriendsTab from "./components/tabs/Friends";
import MessagesTab from "./components/tabs/Messages";
import LeaderboardTab from "./components/tabs/Leaderboard";
import ProfileTab from "./components/tabs/Profile";
import Header from "./components/Header";
import { AuthProvider } from "./context/AuthContext";

import { Route, Routes } from "react-router-dom";
import SelectedGame from "./components/game/SelectedGame";
import TabButtons from "./components/tabs/TabButtons";
function App() {
  return (
    <AuthProvider>
      <Header />
      <TabButtons />
      <Box p="2%">
        <Routes>
          <Route path="/games" element={<GamesTab />} />
          <Route path="/games/:gameId" element={<SelectedGame />} />
          <Route path="/friends" element={<FriendsTab />} />
          <Route path="/messages" element={<MessagesTab />} />
          <Route path="/leaderboard" element={<LeaderboardTab />} />
          <Route path="/profile" element={<ProfileTab />} />
          <Route path="*" element={<GamesTab />} /> {/* should maybe be error page instead? */}
        </Routes>
      </Box>
    </AuthProvider>
  );
}

export default App;
