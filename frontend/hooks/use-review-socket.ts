"use client";

import { useEffect, useRef, useState } from "react";

export interface ReviewMessage {
  type: string;
  payload?: { author?: string; text?: string };
  message?: string;
}

export function useReviewSocket(room: string): {
  messages: ReviewMessage[];
  sendComment: (text: string) => void;
} {
  const [messages, setMessages] = useState<ReviewMessage[]>([]);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000";
    const ws = new WebSocket(`${wsUrl}/ws/review/${room}`);
    socketRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as ReviewMessage;
        setMessages((prev) => [...prev.slice(-50), data]);
      } catch {
        setMessages((prev) => [...prev.slice(-50), { type: "status", message: event.data }]);
      }
    };

    return () => ws.close();
  }, [room]);

  const sendComment = (text: string): void => {
    socketRef.current?.send(JSON.stringify({ author: "current-user", text }));
  };

  return { messages, sendComment };
}
