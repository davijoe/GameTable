import type { Artist } from "./Artist";
import type { Designer } from "./Designer";
import type { Mechanic } from "./Mechanic";
import type { Publisher } from "./Publisher";

export interface GameDetail {
	id: number;
	name: string;
	slug: string | null;
	year_published: number | null;
	bgg_rating: number | null;
	difficulty_rating: number | null;
	description: string | null;
	playing_time: number | null;
	min_players: number | null;
	max_players: number | null;
	image: string | null;
	thumbnail: string | null;

	artists: Artist[];
	designers: Designer[];
	publishers: Publisher[];
	mechanics: Mechanic[];
}