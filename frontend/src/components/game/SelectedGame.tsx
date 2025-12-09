import { useParams } from "react-router-dom";
import {
  VStack,
  Heading,
  Text,
  Box,
  HStack,
  Spinner,
  SimpleGrid,
  Tag,
  Collapse,
  Center,
} from "@chakra-ui/react";
import { useGameDetail } from "../../hooks/useGameDetail";
import GameDetailContributerBox from "./GameDetailBox";
import BackArrow from "../reusable/BackArrow";
import { useState } from "react";

export default function SelectedGame() {
  const { gameId } = useParams<{ gameId: string }>();

  const { data, isLoading, error } = useGameDetail(gameId);
  const [descExpanded, setDescExpanded] = useState(false); //used for description
  console.log("game detail:", data);

  return (
    <Box maxW="900px" mx="auto">
      <BackArrow label="Back to Games" />
      {isLoading && <Center>
        <Spinner size="xl" />
      </Center>}
      {error && <Text color="red.500">{error.message}</Text>}
      {data && (
        <VStack align="stretch" spacing={8}>
          <Box display="flex" flexDir={["column", "row"]} gap={6} w="100%">
            {/* Game Image */}
            <Box
              flexShrink={0}
              w={["100%", "350px"]}
              h={["200px", "350px"]}
              overflow="hidden"
              borderRadius="lg"
              boxShadow="lg"
            >
              <img
                src={data.image || `https://placehold.co/600x800?text=No+Image`}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                }}
              />
            </Box>

            {/* title + stats +  */}
            <VStack align="start" spacing={3}>
              <Heading>{data.name}</Heading>

              <Text fontSize="lg">{data.year_published ?? "N/A"}</Text>

              <HStack spacing={6} wrap="wrap">
                <Box>
                  <Text fontWeight="bold">Rating</Text>
                  <Text>{data.bgg_rating ?? "N/A"}</Text>
                </Box>
                <Box>
                  <Text fontWeight="bold">Play Time</Text>
                  <Text>{data.playing_time} minutes</Text>
                </Box>
                <Box>
                  <Text fontWeight="bold">Players</Text>
                  <Text>
                    {data.min_players}–{data.max_players}
                  </Text>
                </Box>
                <HStack wrap="wrap" spacing={2}>
                  {data.mechanics.map((m) => (
                    <Tag
                      size="md"
                      variant="subtle"
                      colorScheme="purple"
                      borderRadius="full"
                    >
                      {m.name}
                    </Tag>
                  ))}
                </HStack>
              </HStack>
            </VStack>
          </Box>

          {"description"}
          <Box
            p={4}
            borderWidth="1px"
            borderRadius="md"
            cursor="pointer"
            onClick={() => setDescExpanded((prev) => !prev)}
          >
            <Heading size="md" mb={2}>
              Description
            </Heading>

            <Collapse
              in={descExpanded}
              startingHeight="3rem" // height for ~2 lines (adjust based on your lineHeight)
              animateOpacity
            >
              <Text whiteSpace="pre-wrap" lineHeight="1.5rem">
                {data.description}
              </Text>
            </Collapse>
          </Box>

          <SimpleGrid columns={[1, 3]} spacing={4} alignItems={"start"}>
            <GameDetailContributerBox
              title="Designers"
              items={data.designers}
            />
            <GameDetailContributerBox title="Artists" items={data.artists} />
            <GameDetailContributerBox
              title="Publishers"
              items={data.publishers}
            />
          </SimpleGrid>
        </VStack>
      )}
    </Box>
  );
}
