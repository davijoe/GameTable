import { Heading, Image } from "@chakra-ui/react";
import type { Game } from "../../entities/Game";
import { GameCardBase } from "./GameCardBase";

interface Props {
  game: Game;
}

export const GameCard = ({ game }: Props) => {
  return (
    <GameCardBase
      image={
        <Image
          src="/demoGameImgThumbnail.webp"
          objectFit="cover"
        />//hard coded right now - should use the correct when we have that in the DB
      }
    >
      <Heading fontSize="lg">{game.name}</Heading>
      <Heading fontSize="sm" fontWeight="normal" color="gray.400">
        {game.year_published}
      </Heading>
    </GameCardBase>
  );
};