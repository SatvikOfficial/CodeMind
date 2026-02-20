-- DropForeignKey
ALTER TABLE "review_comments" DROP CONSTRAINT "review_comments_parent_id_fkey";

-- DropForeignKey
ALTER TABLE "review_comments" DROP CONSTRAINT "review_comments_thread_id_fkey";

-- DropForeignKey
ALTER TABLE "review_participants" DROP CONSTRAINT "review_participants_room_id_fkey";

-- DropForeignKey
ALTER TABLE "review_threads" DROP CONSTRAINT "review_threads_room_id_fkey";

-- DropIndex
DROP INDEX "idx_analysis_reports_user_created";

-- DropIndex
DROP INDEX "idx_feedback_events_user_created";

-- DropIndex
DROP INDEX "idx_notifications_user_read_created";

-- DropIndex
DROP INDEX "idx_review_threads_room_created";

-- DropIndex
DROP INDEX "idx_user_rules_user_created";

-- AlterTable
ALTER TABLE "analysis_reports" ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3);

-- AlterTable
ALTER TABLE "feedback_events" ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3);

-- AlterTable
ALTER TABLE "notifications" ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3);

-- AlterTable
ALTER TABLE "oauth_connections" ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "expires_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "scopes" DROP DEFAULT,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "updated_at" DROP DEFAULT,
ALTER COLUMN "updated_at" SET DATA TYPE TIMESTAMP(3);

-- AlterTable
ALTER TABLE "review_comments" ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3);

-- AlterTable
ALTER TABLE "review_participants" ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3);

-- AlterTable
ALTER TABLE "review_rooms" ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3);

-- AlterTable
ALTER TABLE "review_threads" ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3);

-- AlterTable
ALTER TABLE "user_rules" ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3);

-- CreateIndex
CREATE INDEX "analysis_reports_user_id_created_at_idx" ON "analysis_reports"("user_id", "created_at");

-- CreateIndex
CREATE INDEX "feedback_events_user_id_created_at_idx" ON "feedback_events"("user_id", "created_at");

-- CreateIndex
CREATE INDEX "notifications_user_id_read_created_at_idx" ON "notifications"("user_id", "read", "created_at");

-- CreateIndex
CREATE INDEX "review_threads_room_id_created_at_idx" ON "review_threads"("room_id", "created_at");

-- CreateIndex
CREATE INDEX "user_rules_user_id_created_at_idx" ON "user_rules"("user_id", "created_at");

-- RenameIndex
ALTER INDEX "idx_oauth_connections_user" RENAME TO "oauth_connections_user_id_idx";

-- RenameIndex
ALTER INDEX "idx_review_comments_thread_created" RENAME TO "review_comments_thread_id_created_at_idx";

-- RenameIndex
ALTER INDEX "idx_review_participants_user" RENAME TO "review_participants_user_id_idx";
