import { redirectToSignIn } from "@clerk/nextjs";
import { redirect } from "next/navigation";

import { currentProfile } from "@/lib/current-profile";
import { db } from "@/lib/db";

interface ServerIdPageProps {
  params: {
    serverId: string;
  }
};

const ServerIdPage = async ({
  params
}: ServerIdPageProps) => {
  // Retrieve the current user's profile
  const profile = await currentProfile();
  //redirec to sign in if the user is not authenticated
  if (!profile) {
    return redirectToSignIn();
  }
   // Check if the server with the given ID exists and the current user is a member
  const server = await db.server.findUnique({
    where: {
      id: params.serverId,
      members: {
        some: {
          profileId: profile.id,
        }
      }
    },
    // Include server channels in the query, specifically the "general" channel
    include: {
      channels: {
        where: {
          name: "general"
        },
        orderBy: {
          createdAt: "asc"
        }
      }
    }
  })
  // Get the first channel (assumed to be the "general" channel) from the server
  const initialChannel = server?.channels[0];
  // If the initial channel is not the "general" channel, return null
  if (initialChannel?.name !== "general") {
    return null;
  }
  // Redirect to the "general" channel of the specified server
  return redirect(`/servers/${params.serverId}/channels/${initialChannel?.id}`)
}
 
export default ServerIdPage;