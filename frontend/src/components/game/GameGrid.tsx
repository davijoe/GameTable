import InfiniteScroll from "react-infinite-scroll-component";
import { useGames } from "../../hooks/useGames";
import { Box, Select, SimpleGrid, Spinner } from "@chakra-ui/react";
import { GameCard } from "./GameCard";
import GameCardContainer from "./GameCardContainer";
import GameCardSkeleton from "./gameCardSkeleton";
import { useState } from "react";
import GameSearchBar from "./GameSearchBar";

type SortField = "bgg_rating" | "year_published" | "playing_time";

export const GameGrid = () => {
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState<SortField>("bgg_rating");
  const {
    data,
    error,
    isLoading,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useGames(search, sortBy);
  if (error) return <p>Error loading games</p>;

  const games = data?.pages.flatMap((page) => page.items) ?? [];
  const skeletons = [...Array(10).keys()];
  return (
    <Box>
      <GameSearchBar value={search} onChange={setSearch} />
      <Select
        w={{ base: "100%", sm: "200px" }}
        value={sortBy}
        onChange={(e) => setSortBy(e.target.value as SortField)}
        variant="filled"
      >
        <option value="bgg_rating">Rating</option>
        <option value="year_published">Year Published</option>
        <option value="playing_time">Playing Time</option>
      </Select>
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
    </Box>
  );
};
