export interface Review {
	id: number;
	title: string;
	text: string | null;
	user: {
		display_name: string;
	};
	star_amount: number;
	game_id: number;
	user_id?: number;
}
