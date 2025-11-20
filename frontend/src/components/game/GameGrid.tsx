import InfiniteScroll from "react-infinite-scroll-component";
import { useGames } from "../../hooks/useGames";

export const GameGrid = () => {
  const { data, error, isLoading, fetchNextPage, hasNextPage } = useGames();

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error loading games</p>;

  const games = data?.pages.flatMap((page) => page.items) ?? [];

  console.log(data?.pages);
    
  return (
    <InfiniteScroll
      dataLength={games.length}
      hasMore={!!hasNextPage}
      next={fetchNextPage}
      loader={<p>Loading more games...</p>}
    >
      <div className="grid grid-cols-4 gap-4">
        {games.map((game) => (
          <div key={game.id} className="p-4 bg-gray-800 rounded-lg">
            <h2 className="font-bold">{game.name}</h2>
            <p>{game.year_published}</p>
          </div>
        ))}
      </div>
    </InfiniteScroll>
  );
};
