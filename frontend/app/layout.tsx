import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import { Space_Grotesk, IBM_Plex_Sans } from "next/font/google";
import type { ReactNode } from "react";

import "@/app/globals.css";
import { Nav } from "@/components/nav";

const headingFont = Space_Grotesk({ subsets: ["latin"], variable: "--font-heading" });
const bodyFont = IBM_Plex_Sans({ subsets: ["latin"], variable: "--font-body", weight: ["400", "500", "600", "700"] });

export const metadata: Metadata = {
  title: "CodeMind",
  description: "AI-powered code quality and collaboration platform"
};

export default function RootLayout({ children }: { children: ReactNode }): JSX.Element {
  return (
    <ClerkProvider>
      <html lang="en" className={`${headingFont.variable} ${bodyFont.variable}`}>
        <body className="font-[var(--font-body)]">
          <Nav />
          <main className="mx-auto max-w-7xl px-4 py-8 md:px-6">{children}</main>
        </body>
      </html>
    </ClerkProvider>
  );
}
