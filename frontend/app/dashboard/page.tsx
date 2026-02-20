import { BarChart3, Gauge, ShieldAlert } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { prisma } from "@/lib/prisma";

export default async function DashboardPage(): Promise<JSX.Element> {
  const [total, highRiskCount, aggregate, recent] = await Promise.all([
    prisma.analysisReport.count().catch(() => 0),
    prisma.analysisReport.count({ where: { score: { lt: 0.5 } } }).catch(() => 0),
    prisma.analysisReport.aggregate({ _avg: { score: true } }).catch(() => ({ _avg: { score: 0 } })),
    prisma.analysisReport
      .findMany({
        orderBy: { createdAt: "desc" },
        take: 5,
        select: { language: true, score: true }
      })
      .catch(() => [])
  ]);

  const stats = {
    total_analyses: total,
    avg_score: aggregate._avg.score ?? 0,
    high_risk_count: highRiskCount,
    recent_languages: recent.map((item) => item.language)
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Team Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardDescription>Total Analyses</CardDescription>
            <CardTitle className="flex items-center justify-between text-3xl">
              {stats.total_analyses}
              <BarChart3 className="h-5 w-5" />
            </CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardDescription>Average Quality</CardDescription>
            <CardTitle className="flex items-center justify-between text-3xl">
              {Math.round(stats.avg_score * 100)}%
              <Gauge className="h-5 w-5" />
            </CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardDescription>High Risk Reports</CardDescription>
            <CardTitle className="flex items-center justify-between text-3xl">
              {stats.high_risk_count}
              <ShieldAlert className="h-5 w-5" />
            </CardTitle>
          </CardHeader>
        </Card>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Recent Languages</CardTitle>
          <CardDescription>Last analyzed language distribution</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {stats.recent_languages.length > 0
              ? stats.recent_languages.map((lang, index) => (
                  <span key={`${lang}-${index}`} className="rounded bg-muted px-3 py-1 text-sm">
                    {lang}
                  </span>
                ))
              : <p className="text-sm text-muted-foreground">No data yet.</p>}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
