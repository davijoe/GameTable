import { useNavigate, useParams } from "react-router-dom";
import {
  VStack,
  Heading,
  Text,
  Box,
  HStack,
  Spinner,
  Accordion,
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  SimpleGrid,
  Tag,
  Collapse,
} from "@chakra-ui/react";
import { useGameDetail } from "../../hooks/useGameDetail";
import GameDetailBox from "./GameDetailBox";
import BackArrow from "../reusable/BackArrow";
import { useState } from "react";

export default function SelectedGame() {
  const { gameId } = useParams<{ gameId: string }>();

  const { data, isLoading, error } = useGameDetail(gameId);
  const [expanded, setExpanded] = useState(false); //used for contributer
  const [descExpanded, setDescExpanded] = useState(false); //used for description
  console.log("game detail:", data);

  return (
    <Box maxW="900px" mx="auto">
      <BackArrow label="Back to Games" />
      {isLoading && <Spinner size="xl" />}
      {error && <Text color="red.500">{error.message}</Text>}
      {data && (
        <VStack align="stretch" spacing={8}>
          {/* Header Section */}
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
            cursor="pointer"
            onClick={() => setDescExpanded((prev) => !prev)}
          >
            <Heading size="md" mb={2}>
              Description
            </Heading>

            <Collapse in={descExpanded} animateOpacity>
              <Text whiteSpace="pre-wrap">{data.description}</Text>
            </Collapse>

            {!descExpanded && (
              <Text
                noOfLines={2} // Chakra will clamp to 2 lines with ellipsis
                whiteSpace="pre-wrap"
              >
                {data.description}
              </Text>
            )}
          </Box>

          <SimpleGrid columns={[1, 3]} spacing={4}>
            <GameDetailBox
              title="Designers"
              items={data.designers}
              expanded={expanded}
              onToggle={() => setExpanded(!expanded)}
            />
            <GameDetailBox
              title="Artists"
              items={data.artists}
              expanded={expanded}
              onToggle={() => setExpanded(!expanded)}
            />
            <GameDetailBox
              title="Publishers"
              items={data.publishers}
              expanded={expanded}
              onToggle={() => setExpanded(!expanded)}
            />
          </SimpleGrid>
        </VStack>
      )}
    </Box>
  );
}
