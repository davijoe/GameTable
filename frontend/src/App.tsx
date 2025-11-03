import { useState } from "react";

import "./App.css";
import { Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/react";
import GamesTab from "./components/tabs/Games";
import FriendsTab from "./components/tabs/Friends";
import MessagesTab from "./components/tabs/Messages";
import LeaderboardTab from "./components/tabs/Leaderboard";
import ProfileTab from "./components/tabs/Profile";
import Header from "./components/Header";

function App() {
  //const [count, setCount] = useState(0);

  return (
    <>
    <Header/>
      <Tabs variant="enclosed">
        <TabList>
          <Tab>Games</Tab>
          <Tab>Friends</Tab>
          <Tab>Messages</Tab>
          <Tab>Leaderboard</Tab>
          <Tab>Profile</Tab>
        </TabList>
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
    </>
  );
}

export default App;
