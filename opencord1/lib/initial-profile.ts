import { currentUser, redirectToSignIn } from "@clerk/nextjs";

import { db } from "@/lib/db";

export const initialProfile = async () => {
  //get current user
  const user = await currentUser();
  //if no current user, go to sing in
  if (!user) {
    return redirectToSignIn();
  }
  //find profile with specific id
  const profile = await db.profile.findUnique({
    where: {
      userId: user.id
    }
  });
  //return if profile exists
  if (profile) {
    return profile;
  }
  //create new profile of user
  const newProfile = await db.profile.create({
    data: {
      userId: user.id,
      name: `${user.firstName} ${user.lastName}`,
      imageUrl: user.imageUrl,
      email: user.emailAddresses[0].emailAddress
    }
  });

  return newProfile;
};
