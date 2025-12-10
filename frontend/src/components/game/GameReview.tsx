import {
  Box,
  Text,
  VStack,
  HStack,
  Button,
  Spinner,
  Center,
  Icon,
  Heading,
} from "@chakra-ui/react";
import { useReviewsByGame } from "../../hooks/useReviewByGame";
import { StarIcon } from "@chakra-ui/icons/Star";

interface GameReviewProps {
  gameId: string;
}

export default function GameReview({ gameId }: GameReviewProps) {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    error,
  } = useReviewsByGame(gameId);


  if (isLoading)
    return (
      <Center>
        <Spinner size="lg" />
      </Center>
    );

  if (error) return <Text color="red.500">{error.message}</Text>;
  if (!data || data.pages.length === 0) return <Text>No reviews yet.</Text>;
  return (
    <Box>
      <HStack p={2}>
          {/*<Heading>{"25"}</Heading>*/}
          <Heading>{"Reviews"}</Heading>
      </HStack>
      <VStack align="stretch" spacing={4}>
        {data.pages.map((page, i) => (
          <Box key={i}>
            {page.items.map((review) => (
              <Box
                key={review.id}
                p={4}
                borderWidth="1px"
                borderRadius="md"
                boxShadow="sm"
              >
                <HStack justify="space-between" mb={2}>
                  <Text fontWeight="bold">{review.user.display_name}</Text>
                  <HStack>
                    {review.star_amount && (
                      <>
                        <Text>{review.star_amount}</Text>
                        <Icon as={StarIcon} color="yellow.300" />
                      </>
                    )}
                  </HStack>
                </HStack>
                <Text whiteSpace="pre-wrap">{review.text}</Text>
                <Text fontSize="sm" color="gray.500" mt={2}></Text>
              </Box>
            ))}
          </Box>
        ))}
        {hasNextPage && (
          <Center mt={2}>
            <Button
              onClick={() => fetchNextPage()}
              isLoading={isFetchingNextPage}
              colorScheme="purple"
            >
              Load 5 More
            </Button>
          </Center>
        )}
      </VStack>
    </Box>
  );
}
