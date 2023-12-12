import { redirectToSignIn } from "@clerk/nextjs";
import { redirect } from "next/navigation";

import { db } from "@/lib/db";
import { currentProfile } from "@/lib/current-profile";

interface InviteCodePageProps {
  params: {
    inviteCode: string;
  };
};

const InviteCodePage = async ({
  params
}: InviteCodePageProps) => {
  //get the current user's profile
  const profile = await currentProfile();

  //redirect so sing in page if the user is not logged in
  if (!profile) {
    return redirectToSignIn();
  }
  //if there is no invide code, redirect to home page
  if (!params.inviteCode) {
    return redirect("/");
  }

  // Check if the server with the given invite code already exists and the current user is a member
  const existingServer = await db.server.findFirst({
    where: {
      inviteCode: params.inviteCode,
      members: {
        some: {
          profileId: profile.id
        }
      }
    }
  });
  // If the server already exists and the user is a member, redirect to the server's page
  if (existingServer) {
    return redirect(`/servers/${existingServer.id}`);
  }
  // If the server does not exist, create it and add the current user as a member
  const server = await db.server.update({
    where: {
      inviteCode: params.inviteCode,
    },
    data: {
      members: {
        create: [
          {
            profileId: profile.id,
          }
        ]
      }
    }
  });
  // If the server was successfully created or updated, redirect to the server's page
  if (server) {
    return redirect(`/servers/${server.id}`);
  }
  
  return null;
}
 
export default InviteCodePage;