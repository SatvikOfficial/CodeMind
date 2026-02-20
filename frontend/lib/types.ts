export interface AnalysisResult {
  id: string;
  suggestions: string[];
  bugs: string[];
  optimizations: string[];
  documentation: string;
  score: number;
  created_at: string;
}

export interface AnalyticsSummary {
  total_analyses: number;
  avg_score: number;
  high_risk_count: number;
  recent_languages: string[];
}

export interface UserRule {
  id: string;
  name: string;
  pattern: string;
  message: string;
  severity: "info" | "warning" | "critical";
  enabled: boolean;
}

export interface AnalysisSummary {
  id: string;
  language: string;
  repository?: string | null;
  score: number;
  created_at: string;
}

export interface OAuthConnection {
  provider: string;
  username: string;
  connected_at: string;
}

export interface ReviewRoom {
  id: string;
  name: string;
  repository?: string | null;
  role: "owner" | "reviewer" | "viewer";
  created_at: string;
}

export interface ReviewThread {
  id: string;
  room_id: string;
  title: string;
  created_by: string;
  created_at: string;
}

export interface ReviewComment {
  id: string;
  thread_id: string;
  parent_id?: string | null;
  body: string;
  author_id: string;
  created_at: string;
}

export interface AppNotification {
  id: string;
  title: string;
  body: string;
  read: boolean;
  created_at: string;
}
