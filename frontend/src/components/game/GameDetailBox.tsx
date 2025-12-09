import { Box, Text, VStack, Collapse, Button } from "@chakra-ui/react";
import { useState, useRef, useEffect } from "react";

interface Item {
  id: number | string;
  name: string;
}

interface Props {
  title: string;
  items: Item[];
  expandTriggerHeight?: number;
  expanded?: boolean;
  onToggle?: () => void;
}

export default function GameDetailBox({
  title,
  items,
  expandTriggerHeight = 120,
  expanded = false,
  onToggle,
}: Props) {
  const [needsCollapse, setNeedsCollapse] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (contentRef.current) {
      const height = contentRef.current.scrollHeight;
      setNeedsCollapse(height > expandTriggerHeight);
    }
  }, [items, expandTriggerHeight]);

  return (
    <Box p={4} borderWidth="1px" borderRadius="md" w="100%">
      <Text align="center" fontWeight="bold" mb={2}>
        {title}
      </Text>
      <Box borderBottomWidth="1px" borderColor="gray.600" mb={2} />
      <Collapse
        in={!needsCollapse || expanded}
        animateOpacity
        style={{ overflow: "hidden" }}
      >
        <VStack ref={contentRef} align="start" spacing={1}>
          {items.map((item) => (
            <Text key={item.id}>{item.name}</Text>
          ))}
        </VStack>
      </Collapse>

      {needsCollapse && (
        <Button
          size="sm"
          mt={2}
          variant="link"
          colorScheme="blue"
          onClick={onToggle}
        >
          {expanded ? "Show Less" : "Show More"}
        </Button>
      )}
    </Box>
  );
}
