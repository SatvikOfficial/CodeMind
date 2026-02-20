import { ReviewsWorkspace } from "@/components/reviews-workspace";

export default function ReviewsPage(): JSX.Element {
  return (
    <div className="space-y-4">
      <h1 className="font-[var(--font-heading)] text-3xl font-bold tracking-tight">Review Workspace</h1>
      <p className="text-sm text-muted-foreground">Persistent review rooms, threaded comments, and role-aware collaboration.</p>
      <ReviewsWorkspace />
    </div>
  );
}
