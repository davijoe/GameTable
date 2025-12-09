import { Box, Input, InputGroup, InputLeftElement, InputRightElement, IconButton } from "@chakra-ui/react";
import { SearchIcon, CloseIcon } from "@chakra-ui/icons";
import { useState, useEffect } from "react";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  debounceTime?: number; // in ms
}

export default function GameSearchBar({ value, onChange, debounceTime = 250 }: SearchBarProps) {
  const [localValue, setLocalValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      onChange(localValue);
    }, debounceTime);

    return () => clearTimeout(handler);
  }, [localValue, onChange, debounceTime]);

  return (
      <InputGroup >
        <InputLeftElement pointerEvents="none">
          <SearchIcon color="gray.400" />
        </InputLeftElement>

        <Input
          placeholder="Search..."
          value={localValue}
          onChange={(e) => setLocalValue(e.target.value)}
          borderRadius="md"
          _focus={{borderColor: "brand.500" }}
        />

        {localValue && (
          <InputRightElement>
            <IconButton
              aria-label="Clear search"
              icon={<CloseIcon />}
              size="sm"
              variant="ghost"
              onClick={() => setLocalValue("")}
            />
          </InputRightElement>
        )}
      </InputGroup>
  );
}
