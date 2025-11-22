export interface Game {
	id: string;
	name: string;
	slug: string | null;
	year_published: string | null;
	bgg_rating: number | null;
	difficulty_rating: number | null;
	description: string | null;
	play_time: number | null;
	available: boolean;
	min_players: number | null;
	max_players: number | null;
}