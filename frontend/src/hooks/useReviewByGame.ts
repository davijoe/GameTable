import { useInfiniteQuery } from "@tanstack/react-query";
import type { PaginatedResponse } from "../services/api-client";
import type { Review } from "../entities/Review";
import { getReviewsByGame } from "../services/review_Service";

export const useReviewsByGame = (gameId: string) =>
	useInfiniteQuery<PaginatedResponse<Review>, Error>({
		queryKey: ["reviews/by-game", gameId],
		queryFn: ({ pageParam = 0 }) => getReviewsByGame(gameId, pageParam as number, 5),
		getNextPageParam: (lastPage) => {
			const nextOffset = lastPage.offset + lastPage.limit;
			return nextOffset < lastPage.total ? nextOffset : undefined;
		},
		initialPageParam: 0,
	});