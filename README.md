# CodeMind

Production-oriented AI code intelligence platform using Bun + Next.js + FastAPI + LangChain + PostgreSQL/Prisma + Redis + WebSockets + Docker.

## Monorepo Layout

- `frontend/`: Next.js 14 app (Tailwind, Clerk, Monaco, dashboard, real-time review UI)
- `backend/`: FastAPI async API (analysis orchestration, Redis cache, WebSocket, analytics)
- `ml_service/`: FastAPI ML inference service (LangChain + NVIDIA API route + HF embeddings + Pinecone)
- `prisma/`: Prisma schema and migrations for PostgreSQL
- `.github/workflows/`: CI and deployment workflow templates

## Quick Start

1. Copy env files and set values:
   - `cp .env.example .env`
   - `cp frontend/.env.example frontend/.env.local`
   - `cp backend/.env.example backend/.env`
   - `cp ml_service/.env.example ml_service/.env`
2. Start stack:
   - `docker compose up --build`
3. Apply database migration:
   - `bunx prisma migrate deploy --schema=prisma/schema.prisma`
4. Open:
   - Frontend: `http://localhost:3000`
   - Backend docs: `http://localhost:8000/docs`
   - ML service health: `http://localhost:8001/health`

## Dev Commands

- Frontend only: `bun --cwd frontend run dev`
- Backend only: `cd backend && uvicorn app.main:app --reload --port 8000`
- ML service only: `cd ml_service && uvicorn app.main:app --reload --port 8001`
- Prisma generate: `bun run prisma:generate`

## Production Notes

- Frontend deploy target: Vercel
- Backend and ML service deploy target: Railway
- Set Clerk issuer/JWKS and disable optional auth in production (`CLERK_OPTIONAL_AUTH=false`)
- Add managed Postgres, Redis, and Pinecone secrets in platform env settings
- Replace placeholder deploy workflow steps with CLI/API deploy commands and secrets

## New API Capabilities

- `POST /analysis`: Runs ML analysis and applies team rule-engine findings.
- `GET /analysis/analytics`: Returns aggregate analysis stats.
- `GET /analysis/recent`: Returns recent analysis report history.
- `GET /rules`: Lists team/user custom rules.
- `POST /rules`: Creates a new custom regex rule.
- `POST /rules/feedback`: Stores feedback for learning signals.
- `GET /oauth/{provider}/start`: Starts OAuth flow (`github`, `gitlab`, `bitbucket`).
- `GET /oauth/{provider}/callback`: OAuth callback endpoint that persists connection.
- `GET /oauth/connections`: Lists connected provider accounts.
- `GET /integrations/{provider}/repos`: Lists repos using persisted OAuth connection.
- `POST /collaboration/rooms`: Creates a review room.
- `POST /collaboration/threads`: Creates a thread in a room.
- `POST /collaboration/comments`: Posts threaded comments with persistence.
- `GET /collaboration/notifications`: Lists user notifications.

## Security Defaults

- Response security headers (CSP, frame protection, mime sniff protection).
- In-memory IP rate limiting middleware (default 180 req/min per client).

## Frontend Workspaces

- `/`: Analyzer workspace with Monaco, ML output, feedback, live review, and custom rules.
- `/integrations`: OAuth connection management and repository sync view.
- `/reviews`: Persistent room/thread/comment collaboration workspace with role checks.
