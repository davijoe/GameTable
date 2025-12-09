import { useQuery } from "@tanstack/react-query";
import type { GameDetail } from "../entities/GameDetail";
import gameDetailService from "../services/game/gameDetailService";

export const useGameDetail = (gameId: string | undefined) =>
	useQuery<GameDetail, Error>({
		queryKey: ["game-detail", gameId],
		queryFn: () => gameDetailService.get(`${gameId}/detail`),
		enabled: !!gameId,
	});