import type { Review } from "../entities/Review";
import ApiClient from "./api-client";



class ReviewApiClient extends ApiClient<Review> {
	async create(data: Partial<Review>, config?: any) {
		return super.create(data, config);
	}
}

const reviewService = new ReviewApiClient("/reviews");

export const getReviewsByGame = (gameId: string, offset = 0, limit = 10) => {
	return reviewService.getAll({
		path: `/gameid/${gameId}`,
		params: { offset, limit },
	});
};

export default reviewService;