import { Box } from "@chakra-ui/react";
import type { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

const GameCardContainer = ({ children }: Props) => {
  return (
    <Box
      _hover={{
        transform: "scale(1.05)",
        transition: "transform 0.2s ease-in-out",
      }}
      overflow="hidden"
      borderRadius={10}
    >
      {children}
    </Box>
  );
};

export default GameCardContainer;