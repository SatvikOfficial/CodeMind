"use client";

import Link from "next/link";
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/nextjs";

import { NotificationCenter } from "@/components/notification-center";
import { Button } from "@/components/ui/button";

const links = [
  { href: "/", label: "Analyzer" },
  { href: "/reviews", label: "Reviews" },
  { href: "/integrations", label: "Integrations" },
  { href: "/dashboard", label: "Analytics" }
];

export function Nav(): JSX.Element {
  return (
    <header className="sticky top-0 z-40 border-b border-border/60 bg-white/70 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 md:px-6">
        <Link href="/" className="font-[var(--font-heading)] text-xl font-bold tracking-tight">
          CodeMind
        </Link>
        <nav className="hidden items-center gap-2 md:flex">
          {links.map((link) => (
            <Link key={link.href} href={link.href} className="rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition hover:bg-muted hover:text-foreground">
              {link.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <SignedIn>
            <NotificationCenter />
          </SignedIn>
          <SignedOut>
            <SignInButton mode="modal">
              <Button size="sm">Sign In</Button>
            </SignInButton>
          </SignedOut>
          <SignedIn>
            <UserButton />
          </SignedIn>
        </div>
      </div>
    </header>
  );
}
