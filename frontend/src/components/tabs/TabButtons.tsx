import { Box, HStack, Button } from "@chakra-ui/react";
import { Link as RouterLink, useLocation } from "react-router-dom";

const tabs = [
	{ label: "Games", path: "/games" },
	{ label: "Friends", path: "/friends" },
	{ label: "Messages", path: "/messages" },
	{ label: "Leaderboard", path: "/leaderboard" },
	{ label: "Profile", path: "/profile" },
];

export default function TabButtons() {
	const location = useLocation();

	return (
		<Box p="2%">
			<Box
				border="1px solid"
				borderColor="whiteAlpha.300"
				borderRadius="full"
				p={1}
				display="inline-flex"
				bg="blackAlpha.300"
			>
				<HStack spacing={2}>
					{tabs.map(tab => (
						<Button
							key={tab.path}
							as={RouterLink}
							to={tab.path}
							variant={location.pathname.startsWith(tab.path) ? "solid" : "ghost"}
							size="lg"
							borderRadius="full"
						>
							{tab.label}
						</Button>
					))}
				</HStack>
			</Box>
		</Box>
	);
}