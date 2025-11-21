import { useState, useRef, useEffect } from "react";
import {
  Button,
  FormControl,
  FormLabel,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Stack,
  Text,
  useDisclosure,
  Box,
  Link,
} from "@chakra-ui/react";
import { useAuth } from "../context/AuthContext";

export default function LoginModal() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { login } = useAuth();
  const [isSignup, setIsSignup] = useState(false);
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    displayName: "",
    email: "",
    dob: "",
  });
  const [error, setError] = useState("");
  const [displayNameError, setDisplayNameError] = useState("");
  const [usernameError, setUsernameError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const debounceRef = useRef<number | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Only validate when signing up
    if (!isSignup) return;

    // Clear any pending validation
    if (debounceRef.current) {
      window.clearTimeout(debounceRef.current);
      debounceRef.current = null;
    }

    // If empty, clear errors immediately
    if (!value) {
      if (name === "displayName") setDisplayNameError("");
      if (name === "username") setUsernameError("");
      return;
    }

    // Debounce validation requests (300ms)
    debounceRef.current = window.setTimeout(async () => {
      try {
        const apiBase = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
        const response = await fetch(
          `${apiBase}/api/users?q=${encodeURIComponent(value)}&limit=200`
        );
        const data = await response.json();

        if (name === "displayName") {
          const exists = data.items.some(
            (user: { display_name: string }) => user.display_name === value
          );
          setDisplayNameError(exists ? "Display name already taken" : "");
        }

        if (name === "username") {
          const exists = data.items.some((user: { username: string }) => user.username === value);
          setUsernameError(exists ? "Username already taken" : "");
        }
      } catch {
        // If validation fetch fails, don't block the user — clear validation errors
        if (name === "displayName") setDisplayNameError("");
        if (name === "username") setUsernameError("");
      }
      debounceRef.current = null;
    }, 300) as unknown as number;
  };

  useEffect(() => {
    return () => {
      if (debounceRef.current) {
        window.clearTimeout(debounceRef.current);
        debounceRef.current = null;
      }
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      if (isSignup) {
        if (displayNameError || usernameError) {
          setError(
            displayNameError
              ? "Display name is already taken"
              : "Username is already taken"
          );
          setIsLoading(false);
          return;
        }

        // Create user
        const apiBase = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
        const response = await fetch(`${apiBase}/api/users`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            display_name: formData.displayName,
            username: formData.username,
            email: formData.email,
            password: formData.password,
            dob: formData.dob,
          }),
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.detail || "Signup failed");
        }

        // Auto-login after signup
        await login(formData.username, formData.password);
        onClose();
        resetForm();
      } else {
        // Login
        await login(formData.username, formData.password);
        onClose();
        resetForm();
      }
    } catch (err) {
      if (err instanceof Error) {
        // Map network error to a clearer message
        if (err.message === "Failed to fetch" || err.message.includes("NetworkError")) {
          setError("Cannot reach backend — is the server running?");
        } else {
          setError(err.message);
        }
      } else {
        setError("Operation failed");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      username: "",
      password: "",
      displayName: "",
      email: "",
      dob: "",
    });
    setError("");
    setDisplayNameError("");
    setUsernameError("");
    setIsSignup(false);
  };

  const handleClose = () => {
    onClose();
    resetForm();
  };

  const toggleMode = () => {
    setIsSignup(!isSignup);
    setError("");
    setDisplayNameError("");
    setUsernameError("");
  };

  return (
    <>
      <Button onClick={onOpen} colorScheme="blue">
        Login
      </Button>

      <Modal isOpen={isOpen} onClose={handleClose} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{isSignup ? "Create Account" : "Login"}</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <form onSubmit={handleSubmit}>
              <Stack spacing={3}>
                {isSignup && (
                  <>
                    <FormControl isRequired>
                      <FormLabel fontSize="sm">Display Name</FormLabel>
                      <Input
                        name="displayName"
                        size="sm"
                        value={formData.displayName}
                        onChange={handleInputChange}
                        placeholder="Display name"
                        isDisabled={isLoading}
                        required
                        borderColor={displayNameError ? "red.500" : undefined}
                      />
                      {displayNameError && (
                        <Text color="red.500" fontSize="xs" mt={1}>
                          {displayNameError}
                        </Text>
                      )}
                    </FormControl>

                    <FormControl>
                      <FormLabel fontSize="sm">Email</FormLabel>
                      <Input
                        name="email"
                        type="email"
                        size="sm"
                        value={formData.email}
                        onChange={handleInputChange}
                        placeholder="email@example.com"
                        isDisabled={isLoading}
                        required
                      />
                    </FormControl>

                    <FormControl>
                      <FormLabel fontSize="sm">Date of Birth</FormLabel>
                      <Input
                        name="dob"
                        type="date"
                        size="sm"
                        value={formData.dob}
                        onChange={handleInputChange}
                        isDisabled={isLoading}
                        required
                      />
                    </FormControl>
                  </>
                )}

                <FormControl isRequired>
                  <FormLabel fontSize="sm">Username</FormLabel>
                  <Input
                    name="username"
                    size="sm"
                    value={formData.username}
                    onChange={handleInputChange}
                    placeholder="Username"
                    isDisabled={isLoading}
                    required
                    borderColor={usernameError ? "red.500" : undefined}
                  />
                  {isSignup && usernameError && (
                    <Text color="red.500" fontSize="xs" mt={1}>
                      {usernameError}
                    </Text>
                  )}
                </FormControl>

                <FormControl>
                  <FormLabel fontSize="sm">Password</FormLabel>
                  <Input
                    name="password"
                    type="password"
                    size="sm"
                    value={formData.password}
                    onChange={handleInputChange}
                    placeholder="Password"
                    isDisabled={isLoading}
                    required
                  />
                </FormControl>

                {error && (
                  <Text color="red.500" fontSize="xs">
                    {error}
                  </Text>
                )}

                <Button
                  type="submit"
                  colorScheme={isSignup ? "green" : "blue"}
                  size="sm"
                  width="100%"
                  isLoading={isLoading}
                  isDisabled={
                    isSignup &&
                    (!!displayNameError ||
                      !!usernameError ||
                      !formData.displayName.trim() ||
                      !formData.username.trim() ||
                      !formData.email.trim() ||
                      !formData.dob.trim() ||
                      !formData.password.trim())
                  }
                >
                  {isSignup ? "Create Account" : "Login"}
                </Button>

                <Box textAlign="center" pt={2}>
                  <Link
                    fontSize="xs"
                    color="blue.500"
                    onClick={toggleMode}
                    cursor="pointer"
                  >
                    {isSignup
                      ? "Already have an account? Login"
                      : "Need an account? Sign up"}
                  </Link>
                </Box>
              </Stack>
            </form>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
}
