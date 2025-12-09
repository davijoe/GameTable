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
  smallHeight = 136, //magic minimum height that "just matches"
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
      _hover={needsCollapse ? { bg: "brand.hover" } : undefined}  // no hover color if can't collapse
      _active={needsCollapse ? { bg: "brand.click" } : undefined}
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
