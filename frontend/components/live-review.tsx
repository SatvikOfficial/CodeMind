"use client";

import { FormEvent, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useReviewSocket } from "@/hooks/use-review-socket";

export function LiveReview(): JSX.Element {
  const { messages, sendComment } = useReviewSocket("default-room");
  const [text, setText] = useState("");

  const onSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!text.trim()) {
      return;
    }
    sendComment(text);
    setText("");
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Live Review Room</CardTitle>
        <CardDescription>Threaded discussion over WebSockets.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="mb-3 h-48 space-y-2 overflow-auto rounded border border-border p-3">
          {messages.map((msg, index) => (
            <p key={index} className="text-sm">
              {msg.type === "comment" ? `${msg.payload?.author}: ${msg.payload?.text}` : msg.message}
            </p>
          ))}
        </div>
        <form onSubmit={onSubmit} className="flex gap-2">
          <input
            className="flex-1 rounded border border-border bg-background px-3 py-2 text-sm"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Post comment"
          />
          <Button type="submit" size="sm">Send</Button>
        </form>
      </CardContent>
    </Card>
  );
}
