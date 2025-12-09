import { useInfiniteQuery } from "@tanstack/react-query";
import type { PaginatedResponse } from "../services/api-client";
import type { Game } from "../entities/Game";
import gameService from "../services/game/gameService";

export const useGames = (q?: string, sortBy?: string) =>
  useInfiniteQuery<PaginatedResponse<Game>, Error>({
    queryKey: ["games", q, sortBy],
    queryFn: ({ pageParam = 0 }) =>
      gameService.getAll({
        params: {
          offset: pageParam,
          limit: 10,
          q,
          sort_by: sortBy,
        },
      }),
    getNextPageParam: (lastPage) => {
      const nextOffset = lastPage.offset + lastPage.limit;
      return nextOffset < lastPage.total ? nextOffset : undefined;
    },
    initialPageParam: 0,
  });
