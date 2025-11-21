import { useNavigate, useParams } from "react-router-dom";
import { VStack, Heading, Text, Box, IconButton } from "@chakra-ui/react";
import { ArrowBackIcon } from "@chakra-ui/icons";

export default function SelectedGame() {
	const { gameId } = useParams<{ gameId: string }>();
	const navigate = useNavigate();

	return (
		<Box p={4}>
			{/* Back button */}
			<IconButton
				icon={<ArrowBackIcon />}
				aria-label="Go back"
				onClick={() => navigate(-1)} // go to previous page
				variant="ghost"
				size="lg"
				mb={4}
			/>

			<VStack align="start" spacing={4}>
				<Heading>Game {gameId}</Heading>
				<Text>Here goes detailed information about the game.</Text>
			</VStack>
		</Box>
	);
}