import { Box } from "@chakra-ui/react";
import type { ReactNode } from "react";
import { useNavigate } from "react-router-dom";

interface Props {
	children: ReactNode;
	gameId?: string; // optional
}

const GameCardContainer = ({ children, gameId }: Props) => {
	const navigate = useNavigate();

	const handleClick = () => {
		if (gameId) {
			navigate(`/games/${gameId}`);
		}
	};

	return (
		<Box
			cursor={gameId ? "pointer" : "default"}
			onClick={handleClick}
			_hover={{
				transform: gameId ? "scale(1.05)" : undefined,
				transition: gameId ? "transform 0.2s ease-in-out" : undefined,
			}}
			overflow="hidden"
			borderRadius={10}
		>
			{children}
		</Box>
	);
};

export default GameCardContainer;