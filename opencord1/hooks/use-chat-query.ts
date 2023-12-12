import qs from "query-string";
import { useInfiniteQuery } from "@tanstack/react-query";

import { useSocket } from "@/components/providers/socket-provider";

interface ChatQueryProps {
  queryKey: string;
  apiUrl: string;
  paramKey: "channelId" | "conversationId";
  paramValue: string;
};

export const useChatQuery = ({
  queryKey,
  apiUrl,
  paramKey,
  paramValue
}: ChatQueryProps) => {
  // Access the socket context to check the connection status
  const { isConnected } = useSocket();

  const fetchMessages = async ({ pageParam = undefined }) => {
    // Construct the URL using the provided API URL and query parameters
    const url = qs.stringifyUrl({
      url: apiUrl,
      query: {
        cursor: pageParam,
        [paramKey]: paramValue,
      }
    }, { skipNull: true });
    // Fetch data from the specified URL
    const res = await fetch(url);
    return res.json();
  };

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    status,
  } = useInfiniteQuery({
    // The query key is an array of values that uniquely identify the query
    queryKey: [queryKey],
    // The query function to fetch data based on the provided parameters
    queryFn: fetchMessages,
    // Function to get the next page cursor from the last page of data
    getNextPageParam: (lastPage) => lastPage?.nextCursor,
    // Refetch interval set to false if the socket is connected, otherwise every 1000 milliseconds
    refetchInterval: isConnected ? false : 1000,
  });

  return {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    status,
  };
}