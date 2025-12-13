import { Heading, HStack, Icon, Image, Text, VStack } from "@chakra-ui/react";
import type { Game } from "../../entities/Game";
import { GameCardBase } from "./GameCardBase";
import { StarIcon, TimeIcon } from "@chakra-ui/icons";

interface Props {
  game: Game;
}

export const GameCard = ({ game }: Props) => {
  return (
    <GameCardBase
      image={
        <Image src={game.thumbnail ?? undefined} objectFit="cover" /> //hard coded right now - should use the correct when we have that in the DB
      }
    >
      <VStack align="start" spacing={2}>
        {/* Title + Year */}
        <HStack spacing={2}>
          <Heading fontSize="lg" noOfLines={1}>
            {game.name}
          </Heading>
          <Text fontSize="sm" color="gray.400" data-testid="game-year">
            {game.year_published || "—"}
          </Text>
        </HStack>
      </VStack>

      {/* Description */}
      <Text fontSize="sm" color="gray.400" noOfLines={3} mt={2} mb={2}>
        {game.description || ""}
      </Text>
      <HStack justifyContent="space-between">
        {/* rating */}
        <HStack spacing={1}>
          <Icon as={StarIcon}  color="yellow.300" />
          <Text fontWeight="bold" data-testid="game-rating">
            {game.bgg_rating ? game.bgg_rating.toFixed(1) : "—"}
          </Text>
        </HStack>

        {/* Play Time */}
        <HStack spacing={2} color="gray.300">
          <Icon as={TimeIcon} />
          <Text data-testid="game-playing-time">
            {game.playing_time ? `${game.playing_time} min` : "—"}
          </Text>
        </HStack>
      </HStack>
    </GameCardBase>
  );
};
