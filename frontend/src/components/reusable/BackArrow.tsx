// BackArrow.tsx
import { HStack, Icon, Text } from "@chakra-ui/react";
import { ArrowBackIcon } from "@chakra-ui/icons";
import { useNavigate } from "react-router-dom";

interface Props {
  label?: string;
}

export default function BackArrow({ label }: Props) {
  const navigate = useNavigate();
  return (
    <HStack
      as="button"
      onClick={() => navigate(-1)}
      mb={6}
      spacing={2}
      cursor="pointer"
      align="center"
      _hover={{ opacity: 0.7 }}
      transition="0.2s"
    >
      <Icon as={ArrowBackIcon} boxSize={6} />
      <Text fontWeight="semibold">{label}</Text>
    </HStack>
  );
}
