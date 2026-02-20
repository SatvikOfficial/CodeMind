"use client";

import { useEffect, useState } from "react";
import { Bell } from "lucide-react";

import { Button } from "@/components/ui/button";
import { listNotifications, markNotificationRead } from "@/lib/api";
import { AppNotification } from "@/lib/types";

export function NotificationCenter(): JSX.Element {
  const [items, setItems] = useState<AppNotification[]>([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    listNotifications().then(setItems).catch(() => setItems([]));
  }, []);

  const unread = items.filter((item) => !item.read).length;

  const markRead = async (id: string) => {
    await markNotificationRead(id);
    setItems((prev) => prev.map((item) => (item.id === id ? { ...item, read: true } : item)));
  };

  return (
    <div className="relative">
      <Button variant="outline" size="sm" onClick={() => setOpen((v) => !v)}>
        <Bell className="h-4 w-4" />
        {unread > 0 ? <span className="ml-2 rounded-full bg-accent px-2 py-0.5 text-xs text-accent-foreground">{unread}</span> : null}
      </Button>
      {open ? (
        <div className="absolute right-0 z-20 mt-2 w-80 rounded-lg border bg-white p-2 shadow-lg">
          {items.length === 0 ? <p className="p-2 text-sm text-muted-foreground">No notifications</p> : null}
          <div className="max-h-72 overflow-auto">
            {items.map((item) => (
              <button
                key={item.id}
                onClick={() => markRead(item.id)}
                className={`w-full rounded p-2 text-left text-sm ${item.read ? "opacity-60" : ""}`}
              >
                <p className="font-medium">{item.title}</p>
                <p className="text-xs text-muted-foreground">{item.body}</p>
              </button>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}
