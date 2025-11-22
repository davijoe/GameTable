import { Box, HStack, Button } from "@chakra-ui/react";
import { Link as RouterLink, useLocation } from "react-router-dom";
const tabs = [
  { label: "Games", path: "/games" },
  { label: "Friends", path: "/friends" },
  { label: "Messages", path: "/messages" },
  { label: "Leaderboard", path: "/leaderboard" },
  { label: "Profile", path: "/profile" },
];

export default function TabButtons() {
  const location = useLocation();

  return (
    <Box p="2%">
      <Box
        border="1px solid"
        borderColor="whiteAlpha.300"
        borderRadius="full"
        p={1}
        display="inline-flex"
        bg="blackAlpha.300"
      >
        <HStack spacing={2}>
          {tabs.map((tab) => {
            const isActive = location.pathname.startsWith(tab.path);
            return (
              <Button
                key={tab.path}
                as={RouterLink}
                to={tab.path}
                size="lg"
                borderRadius="full"
                variant={isActive ? "solid" : "ghost"}
                bg={isActive ? "brand.500" : undefined}
                color={isActive ? "white" : undefined}
                _hover={{
                  bg: isActive ? "brand.500" : "brand.50",
                }}
              >
                {tab.label}
              </Button>
            );
          })}
        </HStack>
      </Box>
    </Box>
  );
}
