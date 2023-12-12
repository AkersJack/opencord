"use client";

import {
  QueryClient,
  QueryClientProvider
} from "@tanstack/react-query";
import { useState } from "react";

export const QueryProvider = ({
  children
}: {
  children: React.ReactNode;
}) => {
  // State variable to hold an instance of the QueryClient
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}