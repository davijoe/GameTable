import InfiniteScroll from "react-infinite-scroll-component";
import { useGames } from "../../hooks/useGames";
import {
  Box,
  HStack,
  IconButton,
  Select,
  SimpleGrid,
  Spinner,
  VStack,
} from "@chakra-ui/react";
import { GameCard } from "./GameCard";
import GameCardContainer from "./GameCardContainer";
import GameCardSkeleton from "./gameCardSkeleton";
import { useState } from "react";
import GameSearchBar from "./GameSearchBar";
import { ArrowUpIcon, ArrowDownIcon } from "@chakra-ui/icons";

type SortField = "bgg_rating" | "year_published" | "playing_time";

export const GameGrid = () => {
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState<SortField>("bgg_rating");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  const {
    data,
    error,
    isLoading,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useGames(search, sortBy, sortOrder);
  if (error) return <p>Error loading games</p>;

  const games = data?.pages.flatMap((page) => page.items) ?? [];
  const skeletons = [...Array(10).keys()];
  return (
    <Box>
      <Box p={3} w={"50%"}>
        <VStack align="start" spacing={3} w="100%">
          <GameSearchBar value={search} onChange={setSearch} />
          <HStack spacing={2}>
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

            <IconButton
              aria-label="Toggle sort order"
              icon={sortOrder === "asc" ? <ArrowUpIcon /> : <ArrowDownIcon />}
              onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
              size="sm"
            />
          </HStack>
        </VStack>
      </Box>
      <InfiniteScroll
        dataLength={games.length}
        hasMore={!!hasNextPage}
        next={fetchNextPage}
        loader={<Spinner data-testid="games-loading-spinner" />}
      >
        <SimpleGrid
          data-testid="game-grid"
          columns={{ base: 1, sm: 3, md: 3, lg: 5 }}
          spacing={5}
          padding={3}
        >
          {isLoading &&
            skeletons.map((id) => (
              <GameCardContainer
                key={`skeleton-initial-${id}`}
                data-testid="game-card-skeleton"
              >
                <GameCardSkeleton />
              </GameCardContainer>
            ))}
          {games.map((game) => (
            <GameCardContainer
              key={game.id}
              gameId={game.id}
              data-testid="game-card"
            >
              <GameCard game={game} />
            </GameCardContainer>
          ))}
          {isFetchingNextPage &&
            skeletons.map((id) => (
              <GameCardContainer
                key={`skeleton-next-${id}`}
                data-testid="game-card-skeleton-next"
              >
                <GameCardSkeleton />
              </GameCardContainer>
            ))}
        </SimpleGrid>
      </InfiniteScroll>
    </Box>
  );
};
