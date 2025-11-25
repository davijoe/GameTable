import {
  Box,
  Button,
  Flex,
  IconButton,
  Text,
} from "@chakra-ui/react";
import { BellIcon } from "@chakra-ui/icons";
import LoginModal from "./LoginModal";
import { useAuth } from "../context/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <Flex
      align="center"
      justify="space-between"
      bg="blackAlpha.300"
      px={8}
      py={4}
      boxShadow="md"
    >
      <Text fontSize="2xl" fontWeight="bold">
        Game Table
      </Text>
      <Flex align="center" gap={5}>
        <IconButton
          aria-label="Notifications"
          icon={<BellIcon />}
          variant="ghost"
          size="md"
        />
        {user ? (
          <>
            <Box
              borderRadius="full"
              bg="blackAlpha.400"
              display="flex"
              padding="10px"
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
