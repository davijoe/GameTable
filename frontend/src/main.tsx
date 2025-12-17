import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import theme from "./theme";

import { ChakraProvider } from "@chakra-ui/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";

type AnyError = {
  status?: number;
  response?: {
    status?: number;
    headers?: Record<string, string>;
  };
};


const isRetryable = (error: AnyError) => {
  const status = error?.status ?? error?.response?.status;

  // If no status, assume network error and retry
  if (!status) return true;

  if (status === 401 || status === 403) return false;
  if (status === 429) return true;
  if (status === 408) return true;
  if (status >= 500 && status <= 599) return true;

  return false; // most 4xx
};


const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,

      retryDelay: (attemptIndex) => {
        const base = Math.min(1000 * 2 ** attemptIndex, 30000);
        const jitter = Math.random() * 300;
        return base + jitter;
      },
      
      staleTime: 1000 * 60 * 5,   // 5min
    },
  },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <ChakraProvider theme={theme}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </ChakraProvider>
    </QueryClientProvider>
  </StrictMode>
);

