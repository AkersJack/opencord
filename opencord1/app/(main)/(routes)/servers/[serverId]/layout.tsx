import { redirectToSignIn } from "@clerk/nextjs";
import { redirect } from "next/navigation";

import { db } from "@/lib/db";
import { currentProfile } from "@/lib/current-profile";
import { ServerSidebar } from "@/components/server/server-sidebar";

const ServerIdLayout = async ({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { serverId: string };
}) => {
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
          profileId: profile.id
        }
      }
    }
  });
  // If the server does not exist or the user is not a member, redirect to the home page
  if (!server) {
    return redirect("/");
  }
  // Render the server layout, including the ServerSidebar and the main content
  return ( 
    <div className="h-full">
      <div 
      className="hidden md:flex h-full w-60 z-20 flex-col fixed inset-y-0">
        <ServerSidebar serverId={params.serverId} />
      </div>
      <main className="h-full md:pl-60">
        {children}
      </main>
    </div>
   );
}
 
export default ServerIdLayout;