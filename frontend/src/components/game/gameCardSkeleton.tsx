import { Skeleton } from "@chakra-ui/react";
import { GameCardBase } from "./GameCardBase";

const GameCardSkeleton = () => {
  return (
    <GameCardBase
      image={<Skeleton width="100%" height="100%" />}
    >
      <Skeleton height="20px" mb="3" />
      <Skeleton height="16px" width="50%" />
    </GameCardBase>
  );
};

export default GameCardSkeleton;