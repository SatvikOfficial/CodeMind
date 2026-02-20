"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, Github, GitBranch, Link2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { listConnections, listProviderRepos, startOAuth } from "@/lib/api";
import { OAuthConnection } from "@/lib/types";

const providers = ["github", "gitlab", "bitbucket"] as const;

type Provider = (typeof providers)[number];

export function IntegrationsWorkspace(): JSX.Element {
  const [connections, setConnections] = useState<OAuthConnection[]>([]);
  const [selectedProvider, setSelectedProvider] = useState<Provider>("github");
  const [repos, setRepos] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  const refresh = async () => {
    const data = await listConnections();
    setConnections(data);
  };

  useEffect(() => {
    refresh().catch(() => setConnections([]));
  }, []);

  const connect = async (provider: Provider) => {
    const authUrl = await startOAuth(provider);
    window.location.href = authUrl;
  };

  const loadRepos = async () => {
    try {
      setError(null);
      const data = await listProviderRepos(selectedProvider);
      setRepos(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed loading repositories");
    }
  };

  const connectedProviders = new Set(connections.map((c) => c.provider));

  return (
    <div className="grid gap-6 lg:grid-cols-[1.2fr,1fr]">
      <Card className="glass shadow-sm">
        <CardHeader>
          <CardTitle className="font-[var(--font-heading)] text-2xl">OAuth Integrations</CardTitle>
          <CardDescription>Connect providers securely and import repositories without manual token paste.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {providers.map((provider) => (
            <div key={provider} className="flex items-center justify-between rounded-lg border p-3">
              <div>
                <p className="font-semibold capitalize">{provider}</p>
                <p className="text-xs text-muted-foreground">OAuth app flow with callback and persisted connection</p>
              </div>
              {connectedProviders.has(provider) ? (
                <span className="inline-flex items-center gap-1 rounded-full bg-emerald-100 px-2 py-1 text-xs text-emerald-700">
                  <CheckCircle2 className="h-3 w-3" /> Connected
                </span>
              ) : (
                <Button size="sm" onClick={() => connect(provider)}>
                  <Link2 className="mr-2 h-4 w-4" /> Connect
                </Button>
              )}
            </div>
          ))}
        </CardContent>
      </Card>

      <Card className="glass shadow-sm">
        <CardHeader>
          <CardTitle className="font-[var(--font-heading)]">Repository Access</CardTitle>
          <CardDescription>Load repositories from connected provider credentials.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <select
            className="w-full rounded border border-border bg-white px-3 py-2 text-sm"
            value={selectedProvider}
            onChange={(e) => setSelectedProvider(e.target.value as Provider)}
          >
            {providers.map((provider) => (
              <option key={provider} value={provider}>{provider}</option>
            ))}
          </select>
          <Button className="w-full" onClick={loadRepos}>
            <GitBranch className="mr-2 h-4 w-4" /> Load Repositories
          </Button>
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          <div className="max-h-72 space-y-1 overflow-auto rounded border bg-white p-2">
            {repos.length === 0 ? <p className="text-sm text-muted-foreground">No repositories loaded.</p> : null}
            {repos.map((repo) => (
              <p key={repo} className="flex items-center gap-2 text-sm"><Github className="h-3.5 w-3.5" />{repo}</p>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
