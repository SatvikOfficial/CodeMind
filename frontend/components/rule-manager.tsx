"use client";

import { FormEvent, useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { createRule, listRules } from "@/lib/api";
import { UserRule } from "@/lib/types";

export function RuleManager(): JSX.Element {
  const [rules, setRules] = useState<UserRule[]>([]);
  const [name, setName] = useState("Avoid eval");
  const [pattern, setPattern] = useState("\\beval\\(");
  const [message, setMessage] = useState("Avoid eval due to injection risk.");
  const [severity, setSeverity] = useState<"info" | "warning" | "critical">("critical");

  useEffect(() => {
    listRules().then(setRules).catch(() => setRules([]));
  }, []);

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const created = await createRule({ name, pattern, message, severity });
    setRules((prev) => [created, ...prev]);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Team Rules</CardTitle>
        <CardDescription>Custom patterns that influence AI analysis output.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <form className="grid gap-2" onSubmit={onSubmit}>
          <input className="rounded border border-border px-3 py-2 text-sm" value={name} onChange={(e) => setName(e.target.value)} />
          <input className="rounded border border-border px-3 py-2 text-sm" value={pattern} onChange={(e) => setPattern(e.target.value)} />
          <input className="rounded border border-border px-3 py-2 text-sm" value={message} onChange={(e) => setMessage(e.target.value)} />
          <select className="rounded border border-border px-3 py-2 text-sm" value={severity} onChange={(e) => setSeverity(e.target.value as "info" | "warning" | "critical")}>
            <option value="info">Info</option>
            <option value="warning">Warning</option>
            <option value="critical">Critical</option>
          </select>
          <Button type="submit" size="sm">Add Rule</Button>
        </form>
        <div className="space-y-2">
          {rules.map((rule) => (
            <div key={rule.id} className="rounded border border-border p-2 text-sm">
              <p className="font-medium">{rule.name} ({rule.severity})</p>
              <p className="text-muted-foreground">/{rule.pattern}/ - {rule.message}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
