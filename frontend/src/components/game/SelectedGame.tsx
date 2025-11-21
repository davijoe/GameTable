import { useParams } from "react-router-dom";
import { VStack, Heading, Text, Box } from "@chakra-ui/react";

export default function SelectedGame() {
	const { gameId } = useParams<{ gameId: string }>();

	return (
		<Box p={4}>
			<VStack align="start" spacing={4}>
				<Heading>Game {gameId}</Heading>
				<Text>Here goes detailed information about the game.</Text>
			</VStack>
		</Box>
	);
}