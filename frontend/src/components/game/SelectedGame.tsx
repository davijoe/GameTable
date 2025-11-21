import { useNavigate, useParams } from "react-router-dom";
import { VStack, Heading, Text, Box, HStack, Icon } from "@chakra-ui/react";
import { ArrowBackIcon } from "@chakra-ui/icons";

export default function SelectedGame() {
  const { gameId } = useParams<{ gameId: string }>();
  const navigate = useNavigate();

  return (
    <Box p={4}>
      <HStack
        as="button"
        onClick={() => navigate(-1)}
        mb={4}
        spacing={2}
        cursor="pointer"
        align="center"
        _hover={{
          bg: "brand.50",
        }}
      >
        <Icon as={ArrowBackIcon} boxSize={6} />
        <Text fontWeight="bold">Back to Games</Text>
      </HStack>

      <VStack align="start" spacing={4}>
        <Heading>Game {gameId}</Heading>
        <Text>Here goes detailed information about the game.</Text>
      </VStack>
    </Box>
  );
}
