import InfiniteScroll from "react-infinite-scroll-component";
import { useGames } from "../../hooks/useGames";
import { SimpleGrid, Spinner } from "@chakra-ui/react";
import { GameCard } from "./GameCard";
import GameCardContainer from "./GameCardContainer";
import GameCardSkeleton from "./gameCardSkeleton";

export const GameGrid = () => {
  const {
    data,
    error,
    isLoading,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useGames();

  if (error) return <p>Error loading games</p>;

  const games = data?.pages.flatMap((page) => page.items) ?? [];

  const skeletons = [...Array(10).keys()];

  return (
    <InfiniteScroll
      dataLength={games.length}
      hasMore={!!hasNextPage}
      next={fetchNextPage}
      loader={<Spinner />}
    >
      <SimpleGrid
        columns={{ base: 1, sm: 3, md: 3, lg: 5 }}
        spacing={5}
        padding={3}
      >
        {isLoading &&
          skeletons.map((id) => (
            <GameCardContainer key={`skeleton-initial-${id}`}>
              <GameCardSkeleton />
            </GameCardContainer>
          ))}

        {games.map((game) => (
          <GameCardContainer key={game.id} gameId={game.id}>
            <GameCard game={game} />
          </GameCardContainer>
        ))}

        {isFetchingNextPage &&
          skeletons.map((id) => (
            <GameCardContainer key={`skeleton-next-${id}`}>
              <GameCardSkeleton />
            </GameCardContainer>
          ))}
      </SimpleGrid>
    </InfiniteScroll>
  );
};
