import "./App.css";
import { Box, Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/react";
import GamesTab from "./components/tabs/Games";
import FriendsTab from "./components/tabs/Friends";
import MessagesTab from "./components/tabs/Messages";
import LeaderboardTab from "./components/tabs/Leaderboard";
import ProfileTab from "./components/tabs/Profile";
import Header from "./components/Header";
import { AuthProvider } from "./context/AuthContext";

function App() {
  //const [count, setCount] = useState(0);

  return (
    <AuthProvider>
      <Header />
      <Box p="2%">
        <Tabs variant="solid-rounded" size="lg">
          <Box
            border="1px solid"
            borderColor="whiteAlpha.300"
            borderRadius="full"
            p={1}
            display="inline-flex"
            bg="blackAlpha.300"
          >
            <TabList gap={2}>
              <Tab>Games</Tab>
              <Tab>Friends</Tab>
              <Tab>Messages</Tab>
              <Tab>Leaderboard</Tab>
              <Tab>Profile</Tab>
            </TabList>
          </Box>
          <TabPanels>
            <TabPanel>
              <GamesTab />
            </TabPanel>
            <TabPanel>
              <FriendsTab />
            </TabPanel>
            <TabPanel>
              <MessagesTab />
            </TabPanel>
            <TabPanel>
              <LeaderboardTab />
            </TabPanel>
            <TabPanel>
              <ProfileTab />
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>
    </AuthProvider>
  );
}

export default App;
