"use client";

import axios from "axios";
import { Check, Copy, RefreshCw } from "lucide-react";
import { useState } from "react";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { useModal } from "@/hooks/use-modal-store";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useOrigin } from "@/hooks/use-origin";

export const InviteModal = () => {
  // Get modal state and data using the useModal hook
  const { onOpen, isOpen, onClose, type, data } = useModal();
  const origin = useOrigin();
  // Check if the modal is open and the type is "invite"
  const isModalOpen = isOpen && type === "invite";
  const { server } = data;
  // State to track if the invite link is copied successfully
  const [copied, setCopied] = useState(false);
  // State to manage loading state during actions
  const [isLoading, setIsLoading] = useState(false);
  // Construct the invite URL using the server's invite code
  const inviteUrl = `${origin}/invite/${server?.inviteCode}`;
  // Function to handle copying the invite link to the clipboard
  const onCopy = () => {
    navigator.clipboard.writeText(inviteUrl);
    setCopied(true);
    // Reset copied state after 1 second
    setTimeout(() => {
      setCopied(false);
    }, 1000);
  };
  // Function to generate a new invite link for the server
  const onNew = async () => {
    try {
      setIsLoading(true);
       // Make a PATCH request to generate a new invite link
      const response = await axios.patch(`/api/servers/${server?.id}/invite-code`);
      // Open a new invite modal with the updated server data
      onOpen("invite", { server: response.data });
    } catch (error) {
      console.log(error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Dialog open={isModalOpen} onOpenChange={onClose}>
      <DialogContent className="bg-white text-black p-0 overflow-hidden">
        <DialogHeader className="pt-8 px-6">
          <DialogTitle className="text-2xl text-center font-bold">
            Invite Friends
          </DialogTitle>
        </DialogHeader>
        <div className="p-6">
          <Label
            className="uppercase text-xs font-bold text-zinc-500 dark:text-secondary/70"
          >
            Server invite link
          </Label>
          <div className="flex items-center mt-2 gap-x-2">
            <Input
              disabled={isLoading}
              className="bg-zinc-300/50 border-0 focus-visible:ring-0 text-black focus-visible:ring-offset-0"
              value={inviteUrl}
            />
            <Button disabled={isLoading} onClick={onCopy} size="icon">
              {copied 
                ? <Check className="w-4 h-4" /> 
                : <Copy className="w-4 h-4" />
              }
            </Button>
          </div>
          <Button
            onClick={onNew}
            disabled={isLoading}
            variant="link"
            size="sm"
            className="text-xs text-zinc-500 mt-4"
          >
            Generate a new link
            <RefreshCw className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}