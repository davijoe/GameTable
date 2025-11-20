import { Box } from "@chakra-ui/react";
import { GameGrid } from "../game/GameGrid";

export default function GamesTab() {

	return (
		<Box p={4}>
			<GameGrid />
		</Box>
	);
}