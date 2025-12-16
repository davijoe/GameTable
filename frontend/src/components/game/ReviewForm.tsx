import { useState } from "react";
import { Box, Button, FormControl, FormLabel, Input, Textarea, VStack, Text, HStack, NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper } from "@chakra-ui/react";
import { useAuth } from "../../context/AuthContext";
import reviewService from "../../services/review_Service";

interface ReviewFormProps {
  gameId: string;
  onReviewSubmitted?: () => void;
}

export default function ReviewForm({ gameId, onReviewSubmitted }: ReviewFormProps) {
  const { user } = useAuth();
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [starAmount, setStarAmount] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  if (!user) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");
    try {
      const access_token = localStorage.getItem("access_token");
      if (!access_token) throw new Error("Not authenticated");
      await reviewService.create(
        {
          title,
          text,
          star_amount: starAmount,
          game_id: Number(gameId),
          user_id: user.id,
        },
        { headers: { Authorization: `Bearer ${access_token}` } }
      );
      setTitle("");
      setText("");
      setStarAmount(5);
      setSuccess("Review submitted!");
      onReviewSubmitted?.();
    } catch (err: any) {
      let msg = err?.response?.data?.detail || err.message || "Failed to submit review";
      // If msg is array (validation errors), join messages
      if (Array.isArray(msg)) {
        msg = msg.map((e: any) => e.msg || JSON.stringify(e)).join("; ");
      } else if (typeof msg === "object") {
        msg = JSON.stringify(msg);
      }
      setError(msg);
      setSuccess("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box borderWidth="1px" borderRadius="md" p={4} mb={4}>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4} align="stretch">
          <FormControl isRequired>
            <FormLabel>Title</FormLabel>
            <Input value={title} onChange={e => setTitle(e.target.value)} maxLength={100} />
          </FormControl>
          <FormControl>
            <FormLabel>Review</FormLabel>
            <Textarea value={text} onChange={e => setText(e.target.value)} maxLength={1000} />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Stars (1-10)</FormLabel>
            <NumberInput min={1} max={10} value={starAmount} onChange={(_, n) => setStarAmount(Number(n))}>
              <NumberInputField />
              <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
              </NumberInputStepper>
            </NumberInput>
          </FormControl>
          {error && <Text color="red.500">{error}</Text>}
          {success && <Text color="green.500">{success}</Text>}
          <HStack justify="flex-end">
            <Button type="submit" colorScheme="purple" isLoading={loading}>
              Submit Review
            </Button>
          </HStack>
        </VStack>
      </form>
    </Box>
  );
}
