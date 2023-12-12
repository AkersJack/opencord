import { db } from "@/lib/db";

export const getOrCreateConversation = async (memberOneId: string, memberTwoId: string) => {
  let conversation = await findConversation(memberOneId, memberTwoId) || await findConversation(memberTwoId, memberOneId);
  // Attempt to find an existing conversation based on memberOneId and memberTwoId
  // If not found, try swapping the memberOneId and memberTwoId and search again
  if (!conversation) {
    conversation = await createNewConversation(memberOneId, memberTwoId);
  }

  return conversation;
}
//find a conversation between two members
const findConversation = async (memberOneId: string, memberTwoId: string) => {
  try {
    // Use Prisma's 'findFirst' to find a conversation with specified memberOneId and memberTwoId
    // Include profiles of both members in the result
    return await db.conversation.findFirst({
      where: {
        AND: [
          { memberOneId: memberOneId },
          { memberTwoId: memberTwoId },
        ]
      },
      include: {
        memberOne: {
          include: {
            profile: true,
          }
        },
        memberTwo: {
          include: {
            profile: true,
          }
        }
      }
    });
  } catch {
    return null;
  }
}
//create a new conversation between two members
const createNewConversation = async (memberOneId: string, memberTwoId: string) => {
  try {
    // Use Prisma's 'create' to add a new conversation with specified memberOneId and memberTwoId
    // Include profiles of both members in the result
    return await db.conversation.create({
      data: {
        memberOneId,
        memberTwoId,
      },
      include: {
        memberOne: {
          include: {
            profile: true,
          }
        },
        memberTwo: {
          include: {
            profile: true,
          }
        }
      }
    })
  } catch {
    return null;
  }
}