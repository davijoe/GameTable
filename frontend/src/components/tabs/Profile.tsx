import {
  Box,
  Text,
  Spinner,
  Alert,
  AlertIcon,
  Stack,
  Avatar,
  Heading,
  Button,
  FormControl,
  FormLabel,
  Input,
  SimpleGrid,
  Divider,
  useColorModeValue,
} from "@chakra-ui/react";

import { useState, useEffect } from "react";

import type { UserProfile } from "../../types/user";

export default function ProfileTab() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [editMode, setEditMode] = useState(false);
  const [editableProfile, setEditableProfile] = useState<UserProfile | null>(
    null
  );
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState<string | null>(null);

  const cardBg = useColorModeValue("white", "gray.800");
  const cardBorder = useColorModeValue("gray.200", "gray.700");

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

  const handleEditClick = () => {
    if (!profile) return;
    setEditableProfile(profile);
    setEditMode(true);
    setSaveError(null);
    setSaveSuccess(null);
  };

  const handleCancelEdit = () => {
    setEditMode(false);
    setEditableProfile(null);
    setSaveError(null);
    setSaveSuccess(null);
  };

  const handleChange = (field: keyof UserProfile, value: string) => {
    setEditableProfile((prev) => (prev ? { ...prev, [field]: value } : prev));
  };

  const handleSave = async () => {
    if (!editableProfile) return;

    const token = localStorage.getItem("access_token");
    if (!token) {
      setSaveError("You are not logged in");
      return;
    }

    setSaving(true);
    setSaveError(null);
    setSaveSuccess(null);

    try {
      const res = await fetch("http://localhost:8000/me", {
        method: "PUT", // adjust to PATCH if your backend expects that
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(editableProfile),
      });

      if (!res.ok) {
        const text = await res.text();
        setSaveError(`Failed to update profile: ${text}`);
        return;
      }

      const updated: UserProfile = await res.json();
      setProfile(updated);
      setEditMode(false);
      setEditableProfile(null);
      setSaveSuccess("Profile updated");
    } catch {
      setSaveError("Network error while updating profile");
    } finally {
      setSaving(false);
    }
  };

  const formatDobForDisplay = (dob?: string) => {
    if (!dob) return "Not set";
    return new Date(dob).toLocaleDateString();
  };

  const formatDobForInput = (dob?: string) => {
    if (!dob) return "";
    try {
      return new Date(dob).toISOString().slice(0, 10);
    } catch {
      return "";
    }
  };

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

  const viewDob = formatDobForDisplay(profile.dob);
  const editDob =
    editableProfile && formatDobForInput(editableProfile.dob as string);

  return (
    <Box p={6} maxW="600px" mx="auto">
      <Box
        bg={cardBg}
        borderWidth="1px"
        borderColor={cardBorder}
        borderRadius="lg"
        p={6}
        boxShadow="sm"
      >
        <Stack direction="row" align="center" spacing={4} mb={4}>
          <Avatar
            size="lg"
            name={profile.display_name || profile.username}
          />
          <Box flex="1">
            <Heading size="md">
              {profile.display_name || profile.username}
            </Heading>
            <Text color="gray.500">@{profile.username}</Text>
          </Box>

          {!editMode && (
            <Button onClick={handleEditClick} variant="solid" colorScheme="blue">
              Edit profile
            </Button>
          )}
        </Stack>

        <Divider mb={4} />

        {saveError && (
          <Alert status="error" mb={4}>
            <AlertIcon />
            {saveError}
          </Alert>
        )}

        {saveSuccess && (
          <Alert status="success" mb={4}>
            <AlertIcon />
            {saveSuccess}
          </Alert>
        )}

        {!editMode && (
          <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
            <Box>
              <Text fontWeight="medium" fontSize="sm" color="gray.500">
                Display name
              </Text>
              <Text fontSize="md">{profile.display_name}</Text>
            </Box>

            <Box>
              <Text fontWeight="medium" fontSize="sm" color="gray.500">
                Username
              </Text>
              <Text fontSize="md">{profile.username}</Text>
            </Box>

            <Box>
              <Text fontWeight="medium" fontSize="sm" color="gray.500">
                Email
              </Text>
              <Text fontSize="md">{profile.email}</Text>
            </Box>

            <Box>
              <Text fontWeight="medium" fontSize="sm" color="gray.500">
                Date of birth
              </Text>
              <Text fontSize="md">{viewDob}</Text>
            </Box>
          </SimpleGrid>
        )}

        {editMode && editableProfile && (
          <Stack spacing={4}>
            <FormControl>
              <FormLabel>Display name</FormLabel>
              <Input
                value={editableProfile.display_name}
                onChange={(e) =>
                  handleChange("display_name", e.target.value)
                }
              />
            </FormControl>

            <FormControl>
              <FormLabel>Username</FormLabel>
              <Input
                value={editableProfile.username}
                onChange={(e) => handleChange("username", e.target.value)}
              />
            </FormControl>

            <FormControl>
              <FormLabel>Email</FormLabel>
              <Input
                type="email"
                value={editableProfile.email}
                onChange={(e) => handleChange("email", e.target.value)}
              />
            </FormControl>

            <FormControl>
              <FormLabel>Date of birth</FormLabel>
              <Input
                type="date"
                value={editDob || ""}
                onChange={(e) => handleChange("dob", e.target.value)}
              />
            </FormControl>

            <Stack direction="row" spacing={3} justify="flex-end" pt={2}>
              <Button variant="ghost" onClick={handleCancelEdit}>
                Cancel
              </Button>
              <Button
                colorScheme="blue"
                onClick={handleSave}
                isLoading={saving}
              >
                Save changes
              </Button>
            </Stack>
          </Stack>
        )}
      </Box>
    </Box>
  );
}
