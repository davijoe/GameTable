import type { Review } from "../entities/Review";
import ApiClient from "./api-client";


const reviewService = new ApiClient<Review>("/reviews");

export const getReviewsByGame = (gameId: string, offset = 0, limit = 10) => {
	return reviewService.getAll({
		path: `/gameid/${gameId}`,
		params: { offset, limit },
	});
};

export default reviewService;