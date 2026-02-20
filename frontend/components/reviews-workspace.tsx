"use client";

import { FormEvent, useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { createComment, createRoom, createThread, listComments, listRooms, listThreads } from "@/lib/api";
import { ReviewComment, ReviewRoom, ReviewThread } from "@/lib/types";

export function ReviewsWorkspace(): JSX.Element {
  const [rooms, setRooms] = useState<ReviewRoom[]>([]);
  const [threads, setThreads] = useState<ReviewThread[]>([]);
  const [comments, setComments] = useState<ReviewComment[]>([]);

  const [selectedRoom, setSelectedRoom] = useState<string>("");
  const [selectedThread, setSelectedThread] = useState<string>("");

  const [roomName, setRoomName] = useState("Main PR Review");
  const [roomRepo, setRoomRepo] = useState("codemind/web");
  const [threadTitle, setThreadTitle] = useState("Security pass for API handlers");
  const [commentText, setCommentText] = useState("Potential auth bypass on optional routes.");

  const refreshRooms = async () => {
    const data = await listRooms();
    setRooms(data);
    if (data.length > 0 && !selectedRoom) {
      setSelectedRoom(data[0].id);
    }
  };

  useEffect(() => {
    refreshRooms().catch(() => setRooms([]));
  }, []);

  useEffect(() => {
    if (!selectedRoom) return;
    listThreads(selectedRoom).then(setThreads).catch(() => setThreads([]));
  }, [selectedRoom]);

  useEffect(() => {
    if (!selectedThread) return;
    listComments(selectedThread).then(setComments).catch(() => setComments([]));
  }, [selectedThread]);

  const onCreateRoom = async (event: FormEvent) => {
    event.preventDefault();
    const room = await createRoom(roomName, roomRepo);
    setRooms((prev) => [room, ...prev]);
    setSelectedRoom(room.id);
  };

  const onCreateThread = async (event: FormEvent) => {
    event.preventDefault();
    if (!selectedRoom) return;
    const thread = await createThread(selectedRoom, threadTitle);
    setThreads((prev) => [thread, ...prev]);
    setSelectedThread(thread.id);
  };

  const onCreateComment = async (event: FormEvent) => {
    event.preventDefault();
    if (!selectedThread) return;
    const comment = await createComment(selectedThread, commentText);
    setComments((prev) => [...prev, comment]);
    setCommentText("");
  };

  return (
    <div className="grid gap-4 lg:grid-cols-[1.1fr,1fr,1.1fr]">
      <Card className="glass shadow-sm">
        <CardHeader>
          <CardTitle>Review Rooms</CardTitle>
          <CardDescription>Persistent spaces with role-based membership.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <form className="grid gap-2" onSubmit={onCreateRoom}>
            <input className="rounded border bg-white px-3 py-2 text-sm" value={roomName} onChange={(e) => setRoomName(e.target.value)} />
            <input className="rounded border bg-white px-3 py-2 text-sm" value={roomRepo} onChange={(e) => setRoomRepo(e.target.value)} />
            <Button type="submit" size="sm">Create Room</Button>
          </form>
          <div className="space-y-2">
            {rooms.map((room) => (
              <button
                key={room.id}
                onClick={() => setSelectedRoom(room.id)}
                className={`w-full rounded border p-2 text-left ${selectedRoom === room.id ? "border-primary" : ""}`}
              >
                <p className="font-medium">{room.name}</p>
                <p className="text-xs text-muted-foreground">{room.repository} • {room.role}</p>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card className="glass shadow-sm">
        <CardHeader>
          <CardTitle>Threads</CardTitle>
          <CardDescription>Structured discussion per room.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <form className="grid gap-2" onSubmit={onCreateThread}>
            <input className="rounded border bg-white px-3 py-2 text-sm" value={threadTitle} onChange={(e) => setThreadTitle(e.target.value)} />
            <Button type="submit" size="sm">Create Thread</Button>
          </form>
          <div className="space-y-2">
            {threads.map((thread) => (
              <button
                key={thread.id}
                onClick={() => setSelectedThread(thread.id)}
                className={`w-full rounded border p-2 text-left ${selectedThread === thread.id ? "border-primary" : ""}`}
              >
                <p className="font-medium">{thread.title}</p>
                <p className="text-xs text-muted-foreground">By {thread.created_by}</p>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card className="glass shadow-sm">
        <CardHeader>
          <CardTitle>Comments</CardTitle>
          <CardDescription>Threaded comments with persistence and notifications.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="max-h-72 space-y-2 overflow-auto rounded border bg-white p-2">
            {comments.length === 0 ? <p className="text-sm text-muted-foreground">No comments in this thread yet.</p> : null}
            {comments.map((comment) => (
              <div key={comment.id} className="rounded border p-2">
                <p className="text-sm">{comment.body}</p>
                <p className="text-xs text-muted-foreground">{comment.author_id}</p>
              </div>
            ))}
          </div>
          <form className="grid gap-2" onSubmit={onCreateComment}>
            <textarea
              className="min-h-24 rounded border bg-white px-3 py-2 text-sm"
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
            />
            <Button type="submit" size="sm">Post Comment</Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
