// Header.tsx
import { Box, Button, Flex, Text } from "@chakra-ui/react";
import { useState, useEffect } from "react";
import LoginModal from "./LoginModal";
import { useAuth } from "../context/AuthContext";
import TabButtons from "./tabs/TabButtons";
import { useNavigate } from "react-router-dom";

interface HeaderProps {
  height?: string;
}

export default function Header({ height = "80px" }: HeaderProps) {
  const { user, logout } = useAuth();
  const [scrolled, setScrolled] = useState(false);
  const navigate = useNavigate();

  //used to change color of header when user scroll
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 0);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <Flex
      align="center"
      justify="space-between"
      px={8}
      py={3}
      position="fixed" // always pinned at the top
      top={0}
      left={0}
      right={0}
      zIndex={100}
      bg={scrolled ? "blackAlpha.800" : "blackAlpha.300"} // color change after scroll
      transition="background 0.2s"
      height={height}
    >
      <Text
        fontSize="2xl"
        fontWeight="bold"
        onClick={() => navigate("/games")}
        cursor={"pointer"}
      >
        Game Table
      </Text>

      <Box>
        <TabButtons />
      </Box>

      <Flex align="center" gap={5}>
        {user ? (
          <>
            <Box
              borderRadius="full"
              bg="blackAlpha.400"
              display="flex"
              padding={"10px"}
            >
              <Text fontSize="sm" fontWeight="semibold" color="white">
                {user.display_name}
              </Text>
            </Box>
            <Button colorScheme="red" onClick={logout}>
              Logout
            </Button>
          </>
        ) : (
          <LoginModal />
        )}
      </Flex>
    </Flex>
  );
}
