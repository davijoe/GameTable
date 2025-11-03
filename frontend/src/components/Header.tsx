import {
  Box,
  Button,
  Flex,
  IconButton,
  Text,
  useColorModeValue,
} from "@chakra-ui/react";
import { BellIcon } from "@chakra-ui/icons";

export default function Header() {
  const bg = useColorModeValue("gray.500", "gray.700");

  return (
    <Flex
      align="center"
      justify="space-between"
      bg={bg}
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
        <Box
          borderRadius="full"
          bg="blackAlpha.500"
          display="flex"
          padding="9px"
        >
          <Text fontSize="sm" fontWeight="semibold" color="white">
            Username
          </Text>
        </Box>
        <Button colorScheme="red">Logout</Button>
      </Flex>
    </Flex>
  );
}
