import { Box, Text, VStack, Collapse } from "@chakra-ui/react";
import { useState, useRef, useEffect } from "react";

interface Item {
  id: number | string;
  name: string;
}

interface Props {
  title: string;
  items: Item[];
  smallHeight?: number; // collapsed height in px
}

export default function GameDetailContributerBox({
  title,
  items,
  smallHeight = 132, //magic minimum height that "just matches"
}: Props) {
  const [expanded, setExpanded] = useState(false);
  const [needsCollapse, setNeedsCollapse] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (contentRef.current) {
      const height = contentRef.current.scrollHeight;
      setNeedsCollapse(height > smallHeight);
    }
  }, [items, smallHeight]);

  return (
    <Box
      p={4}
      borderWidth="1px"
      borderRadius="md"
      w="100%"
      cursor={needsCollapse ? "pointer" : "default"}
      onClick={() => needsCollapse && setExpanded(!expanded)}
      position="relative"
    >
      <Text fontWeight="bold" mb={2} size="md">
        {title}
      </Text>

      <Collapse
        in={expanded || !needsCollapse}
        startingHeight={smallHeight}
        animateOpacity
      >
        <VStack ref={contentRef} align="start" spacing={1}>
          {items.map((item) => (
            <Text key={item.id}>{item.name}</Text>
          ))}
        </VStack>
      </Collapse>

      {/* Gradient overlay for collapsed state */}
      {needsCollapse && !expanded && (
        <Box
          position="absolute"
          bottom={0}
          left={0}
          right={0}
          h="40px"
          bgGradient="linear(to-b, rgba(255, 255, 255, 0), rgba(255,255,255,0.10))"
          pointerEvents="none"
        />
      )}
    </Box>
  );
}
