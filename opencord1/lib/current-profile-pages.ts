import { NextApiRequest } from "next";
import { getAuth } from "@clerk/nextjs/server";

import { db } from "@/lib/db";

export const currentProfilePages = async (req: NextApiRequest) => {
  const { userId } = getAuth(req);

  if (!userId) {
    return null;
  }
  //return user profile with the specific id
  const profile = await db.profile.findUnique({
    where: {
      userId
    }
  });

  return profile;
}