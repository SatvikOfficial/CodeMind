import {
  AnalysisResult,
  AnalysisSummary,
  AnalyticsSummary,
  AppNotification,
  OAuthConnection,
  ReviewComment,
  ReviewRoom,
  ReviewThread,
  UserRule
} from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function runAnalysis(code: string, language: string): Promise<AnalysisResult> {
  const response = await fetch(`${API_URL}/analysis`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ code, language })
  });

  if (!response.ok) {
    throw new Error(`Analysis failed: ${response.status}`);
  }

  return response.json();
}

export async function getAnalytics(): Promise<AnalyticsSummary> {
  const response = await fetch(`/api/analytics`, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Failed to load analytics: ${response.status}`);
  }

  return response.json();
}

export async function listRules(): Promise<UserRule[]> {
  const response = await fetch(`${API_URL}/rules`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to list rules: ${response.status}`);
  }
  return response.json();
}

export async function createRule(payload: Omit<UserRule, "id" | "enabled">): Promise<UserRule> {
  const response = await fetch(`${API_URL}/rules`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    throw new Error(`Failed to create rule: ${response.status}`);
  }
  return response.json();
}

export async function submitFeedback(analysisId: string, accepted: boolean): Promise<void> {
  const response = await fetch(`${API_URL}/rules/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ analysis_id: analysisId, accepted })
  });
  if (!response.ok) {
    throw new Error(`Failed to submit feedback: ${response.status}`);
  }
}

export async function getRecentReports(): Promise<AnalysisSummary[]> {
  const response = await fetch(`${API_URL}/analysis/recent`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to fetch recent reports: ${response.status}`);
  }
  return response.json();
}

export async function startOAuth(provider: "github" | "gitlab" | "bitbucket"): Promise<string> {
  const response = await fetch(`${API_URL}/oauth/${provider}/start`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to start OAuth: ${response.status}`);
  }
  const data = await response.json();
  return data.authorization_url;
}

export async function listConnections(): Promise<OAuthConnection[]> {
  const response = await fetch(`${API_URL}/oauth/connections`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to list connections: ${response.status}`);
  }
  return response.json();
}

export async function listProviderRepos(provider: "github" | "gitlab" | "bitbucket"): Promise<string[]> {
  const response = await fetch(`${API_URL}/integrations/${provider}/repos`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to fetch repos: ${response.status}`);
  }
  const data = await response.json();
  return data.repositories ?? [];
}

export async function listRooms(): Promise<ReviewRoom[]> {
  const response = await fetch(`${API_URL}/collaboration/rooms`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to fetch rooms: ${response.status}`);
  }
  return response.json();
}

export async function createRoom(name: string, repository?: string): Promise<ReviewRoom> {
  const response = await fetch(`${API_URL}/collaboration/rooms`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, repository })
  });
  if (!response.ok) {
    throw new Error(`Failed to create room: ${response.status}`);
  }
  return response.json();
}

export async function listThreads(roomId: string): Promise<ReviewThread[]> {
  const response = await fetch(`${API_URL}/collaboration/rooms/${roomId}/threads`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to fetch threads: ${response.status}`);
  }
  return response.json();
}

export async function createThread(roomId: string, title: string): Promise<ReviewThread> {
  const response = await fetch(`${API_URL}/collaboration/threads`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ room_id: roomId, title })
  });
  if (!response.ok) {
    throw new Error(`Failed to create thread: ${response.status}`);
  }
  return response.json();
}

export async function listComments(threadId: string): Promise<ReviewComment[]> {
  const response = await fetch(`${API_URL}/collaboration/threads/${threadId}/comments`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to fetch comments: ${response.status}`);
  }
  return response.json();
}

export async function createComment(threadId: string, body: string, parentId?: string): Promise<ReviewComment> {
  const response = await fetch(`${API_URL}/collaboration/comments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ thread_id: threadId, body, parent_id: parentId ?? null })
  });
  if (!response.ok) {
    throw new Error(`Failed to create comment: ${response.status}`);
  }
  return response.json();
}

export async function listNotifications(): Promise<AppNotification[]> {
  const response = await fetch(`${API_URL}/collaboration/notifications`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to fetch notifications: ${response.status}`);
  }
  return response.json();
}

export async function markNotificationRead(notificationId: string): Promise<void> {
  const response = await fetch(`${API_URL}/collaboration/notifications/${notificationId}/read`, {
    method: "POST"
  });
  if (!response.ok) {
    throw new Error(`Failed to update notification: ${response.status}`);
  }
}
