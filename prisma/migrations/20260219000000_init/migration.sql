CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS analysis_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  language TEXT NOT NULL,
  repository TEXT,
  code TEXT NOT NULL,
  suggestions JSONB NOT NULL,
  bugs JSONB NOT NULL,
  optimizations JSONB NOT NULL,
  documentation TEXT NOT NULL,
  score DOUBLE PRECISION NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_analysis_reports_user_created
ON analysis_reports (user_id, created_at DESC);
