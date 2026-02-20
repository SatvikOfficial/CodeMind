import { IntegrationsWorkspace } from "@/components/integrations-workspace";

export default function IntegrationsPage(): JSX.Element {
  return (
    <div className="space-y-4">
      <h1 className="font-[var(--font-heading)] text-3xl font-bold tracking-tight">Integrations</h1>
      <p className="text-sm text-muted-foreground">OAuth connections, synced repositories, and provider account status.</p>
      <IntegrationsWorkspace />
    </div>
  );
}
