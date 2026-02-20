import { NextResponse } from "next/server";

import { prisma } from "@/lib/prisma";

export async function GET(): Promise<NextResponse> {
  try {
    const [total, highRiskCount, aggregate, recent] = await Promise.all([
      prisma.analysisReport.count(),
      prisma.analysisReport.count({ where: { score: { lt: 0.5 } } }),
      prisma.analysisReport.aggregate({ _avg: { score: true }, _count: { _all: true } }),
      prisma.analysisReport.findMany({
        orderBy: { createdAt: "desc" },
        take: 5,
        select: { language: true, score: true }
      })
    ]);

    return NextResponse.json({
      total_analyses: total,
      avg_score: aggregate._avg.score ?? 0,
      high_risk_count: highRiskCount,
      recent_languages: recent.map((item) => item.language)
    });
  } catch {
    return NextResponse.json(
      {
        total_analyses: 0,
        avg_score: 0,
        high_risk_count: 0,
        recent_languages: []
      },
      { status: 200 }
    );
  }
}
