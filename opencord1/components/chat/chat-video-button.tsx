"use client";

import qs from "query-string";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { Video, VideoOff } from "lucide-react";


import { ActionTooltip } from "@/components/action-tooltip";

export const ChatVideoButton = () => {
  const pathname = usePathname();
  const router = useRouter();
  const searchParams = useSearchParams();
  // Check if the "video" parameter is present in the search parameters
  const isVideo = searchParams?.get("video");

  const onClick = () => {
    const url = qs.stringifyUrl({
      // Toggle the "video" parameter in the query string
      url: pathname || "",
      query: {
        video: isVideo ? undefined : true,
      }
    }, { skipNull: true });
    // Update the URL and trigger a router navigation
    router.push(url);
  }
  // Choose the appropriate video icon based on whether video is active or not
  const Icon = isVideo ? VideoOff : Video;
  // Define the tooltip label based on the video state
  const tooltipLabel = isVideo ? "End video call" : "Start video call";
  // Render the video button with the chosen icon and tooltip
  return (
    <ActionTooltip side="bottom" label={tooltipLabel}>
      <button onClick={onClick} className="hover:opacity-75 transition mr-4">
        <Icon className="h-6 w-6 text-zinc-500 dark:text-zinc-400" />
      </button>
    </ActionTooltip>
  )
}