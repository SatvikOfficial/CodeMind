"use client";

import { useEffect, useState } from "react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { getRecentReports } from "@/lib/api";
import { AnalysisSummary } from "@/lib/types";

export function RecentReports(): JSX.Element {
  const [reports, setReports] = useState<AnalysisSummary[]>([]);

  useEffect(() => {
    getRecentReports().then(setReports).catch(() => setReports([]));
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Reports</CardTitle>
        <CardDescription>Latest analysis history for quick context.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        {reports.length === 0 ? <p className="text-sm text-muted-foreground">No reports yet.</p> : null}
        {reports.map((report) => (
          <div key={report.id} className="rounded border border-border p-2 text-sm">
            <p className="font-medium">{report.language} • {Math.round(report.score * 100)}%</p>
            <p className="text-xs text-muted-foreground">{new Date(report.created_at).toLocaleString()}</p>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
