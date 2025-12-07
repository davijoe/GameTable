import { useEffect, useState } from "react";
import { Box, Text, Spinner, Alert, AlertIcon, Stack } from "@chakra-ui/react";
import type { UserProfile } from "../../types/user";

export default function ProfileTab() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setError("You are not logged in");
      setLoading(false);
      return;
    }

    const fetchProfile = async () => {
      try {
        const res = await fetch("http://localhost:8000/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) {
          const text = await res.text();
          setError(`Failed to load profile: ${text}`);
          setLoading(false);
          return;
        }

        const data: UserProfile = await res.json();
        setProfile(data);
      } catch {
        setError("Network error while loading profile");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) {
    return (
      <Box p={4}>
        <Spinner mr={2} />
        <Text as="span">Loading profile...</Text>
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={4}>
        <Alert status="error">
          <AlertIcon />
          {error}
        </Alert>
      </Box>
    );
  }

  if (!profile) {
    return (
      <Box p={4}>
        <Text>No profile data available.</Text>
      </Box>
    );
  }

  const dobFormatted = new Date(profile.dob).toLocaleDateString();

  return (
    <Box p={4}>
      <Text fontSize="2xl" fontWeight="bold" mb={4}>
        Profile
      </Text>

      <Stack spacing={2}>
        <Box>
          <Text fontWeight="medium">Display name</Text>
          <Text>{profile.display_name}</Text>
        </Box>

        <Box>
          <Text fontWeight="medium">Username</Text>
          <Text>{profile.username}</Text>
        </Box>

        <Box>
          <Text fontWeight="medium">Email</Text>
          <Text>{profile.email}</Text>
        </Box>

        <Box>
          <Text fontWeight="medium">Date of birth</Text>
          <Text>{dobFormatted}</Text>
        </Box>
      </Stack>
    </Box>
  );
}
