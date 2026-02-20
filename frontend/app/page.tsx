"use client";

import Link from "next/link";
import { useState } from "react";
import { Editor } from "@monaco-editor/react";
import { ArrowRight, Bug, FileText, Lightbulb, Loader2, ThumbsDown, ThumbsUp, Zap } from "lucide-react";

import { LiveReview } from "@/components/live-review";
import { RecentReports } from "@/components/recent-reports";
import { RuleManager } from "@/components/rule-manager";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { runAnalysis, submitFeedback } from "@/lib/api";
import { AnalysisResult } from "@/lib/types";

export default function HomePage(): JSX.Element {
  const [language, setLanguage] = useState("typescript");
  const [code, setCode] = useState("export function sum(a: number, b: number) { return a + b; }");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await runAnalysis(code, language);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <section className="glass rounded-2xl border p-6 shadow-sm md:p-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="mb-1 text-xs font-semibold uppercase tracking-[0.2em] text-muted-foreground">Platform</p>
            <h1 className="font-[var(--font-heading)] text-3xl font-bold tracking-tight md:text-4xl">AI Code Intelligence for Teams</h1>
            <p className="mt-2 max-w-3xl text-sm text-muted-foreground">
              Analyze code, enforce team rules, collaborate in threaded review rooms, and connect repositories through OAuth-backed providers.
            </p>
          </div>
          <div className="flex gap-2">
            <Link href="/reviews"><Button variant="outline">Open Reviews</Button></Link>
            <Link href="/integrations"><Button>Manage Integrations <ArrowRight className="ml-2 h-4 w-4" /></Button></Link>
          </div>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-[1.4fr,1fr]">
        <Card className="glass shadow-sm">
          <CardHeader>
            <CardTitle className="font-[var(--font-heading)] text-2xl">Intelligent Code Analysis</CardTitle>
            <CardDescription>Semantic insights, vulnerabilities, docs, and optimization recommendations.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-2">
              <Badge>Language</Badge>
              <select
                className="rounded border border-border bg-white px-3 py-2 text-sm"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              >
                <option value="typescript">TypeScript</option>
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
              </select>
            </div>
            <Editor
              height="450px"
              language={language}
              value={code}
              onChange={(value) => setCode(value ?? "")}
              theme="vs-dark"
              options={{ minimap: { enabled: false }, fontSize: 14 }}
            />
            {error ? (
              <Alert className="border-red-300">
                <AlertTitle>Analysis Error</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            ) : null}
          </CardContent>
          <CardFooter>
            <Button onClick={handleAnalyze} className="w-full" disabled={loading}>
              {loading ? (
                <span className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Running analysis...
                </span>
              ) : (
                "Analyze Code"
              )}
            </Button>
          </CardFooter>
        </Card>

        <div className="space-y-6">
          <Card className="glass shadow-sm">
            <CardHeader>
              <CardTitle>Analysis Output</CardTitle>
              <CardDescription>Actionable guidance tailored by ML + team rules.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {!result ? <p className="text-sm text-muted-foreground">Run analysis to view findings.</p> : null}
              {result ? (
                <>
                  <Badge>Quality Score: {Math.round(result.score * 100)}%</Badge>
                  {result.suggestions.map((item, idx) => (
                    <Alert key={`s-${idx}`}>
                      <AlertTitle className="flex items-center gap-2"><Lightbulb className="h-4 w-4" />Suggestion</AlertTitle>
                      <AlertDescription>{item}</AlertDescription>
                    </Alert>
                  ))}
                  {result.bugs.map((item, idx) => (
                    <Alert key={`b-${idx}`} className="border-red-300">
                      <AlertTitle className="flex items-center gap-2"><Bug className="h-4 w-4" />Bug Risk</AlertTitle>
                      <AlertDescription>{item}</AlertDescription>
                    </Alert>
                  ))}
                  {result.optimizations.map((item, idx) => (
                    <Alert key={`o-${idx}`}>
                      <AlertTitle className="flex items-center gap-2"><Zap className="h-4 w-4" />Optimization</AlertTitle>
                      <AlertDescription>{item}</AlertDescription>
                    </Alert>
                  ))}
                  <Alert>
                    <AlertTitle className="flex items-center gap-2"><FileText className="h-4 w-4" />Documentation</AlertTitle>
                    <AlertDescription>{result.documentation}</AlertDescription>
                  </Alert>
                  <div className="grid grid-cols-2 gap-2">
                    <Button size="sm" variant="outline" onClick={() => submitFeedback(result.id, true)}>
                      <ThumbsUp className="mr-2 h-4 w-4" /> Useful
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => submitFeedback(result.id, false)}>
                      <ThumbsDown className="mr-2 h-4 w-4" /> Needs Work
                    </Button>
                  </div>
                </>
              ) : null}
            </CardContent>
          </Card>

          <RecentReports />
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <LiveReview />
        <RuleManager />
      </div>
    </div>
  );
}
