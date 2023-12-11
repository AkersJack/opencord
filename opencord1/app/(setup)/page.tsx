import { redirect } from "next/navigation";

import { db } from "@/lib/db";
import { initialProfile } from "@/lib/initial-profile";
import { InitialModal } from "@/components/modals/initial-modal";

const SetupPage = async () => {
  //get the current user's profile
  const profile = await initialProfile();
  // Find the first server where the current user is a member
  const server = await db.server.findFirst({
    where: {
      members: {
        some: {
          profileId: profile.id
        }
      }
    }
  });
  // If the user is a member of a server, redirect to that server's page
  if (server) {
    return redirect(`/servers/${server.id}`);
  }

  return <InitialModal />;
}
 
export default SetupPage;