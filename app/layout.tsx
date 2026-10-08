import type { Metadata } from "next";
import "./globals.css";
import { PwaManager } from "@/components/pwa/PwaManager";
import { site } from "@/lib/site";
import { ContentGuard, Watermark } from "@/components/lesson/ContentGuard";

const BASE = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

export const viewport = {
  themeColor: "#141413",
  width: "device-width",
  initialScale: 1,
};

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: {
    default: `${site.name} o‘zbek tilida — bepul, professional darajada`,
    template: `%s · ${site.name}`,
  },
  description: site.description,
  keywords: [
    "Claude Code",
    "Claude Code o'zbekcha",
    "Claude Code kursi",
    "Claude Code qanday ishlatiladi",
    "Claude Code nima",
    "Anthropic Claude",
    "AI bilan dasturlash",
    "AI agent",
    "sun'iy intellekt dasturlash",
    "CLAUDE.md",
    "MCP",
    "hooks",
    "subagent",
    "o'zbek tilida",
    "bepul kurs",
    "dasturlash",
  ],
  authors: [{ name: site.author.name, url: site.author.portfolio }],
  creator: site.author.name,
  category: "education",
  openGraph: {
    type: "website",
    locale: "uz_UZ",
    url: site.url,
    siteName: site.name,
    title: `${site.name} o‘zbek tilida — bepul, professional darajada`,
    description: site.description,
    images: [{ url: "/og.png", width: 1200, height: 630, alt: site.name }],
  },
  twitter: {
    card: "summary_large_image",
    title: `${site.name} o‘zbek tilida — bepul, professional darajada`,
    description: site.description,
    images: ["/og.png"],
  },
  manifest: `${BASE}/manifest.webmanifest`,
  appleWebApp: {
    capable: true,
    title: "Claude Code",
    statusBarStyle: "black-translucent",
  },
  robots: site.protection.noindex
    ? { index: false, follow: false, nocache: true, googleBot: { index: false, follow: false } }
    : {
        index: true,
        follow: true,
        googleBot: { index: true, follow: true, "max-image-preview": "large", "max-snippet": -1 },
      },
  icons: {
    icon: [
      { url: `${BASE}/icon-192.png`, sizes: "192x192", type: "image/png" },
      { url: `${BASE}/icon.svg`, type: "image/svg+xml" },
    ],
    apple: `${BASE}/apple-touch-icon.png`,
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="uz">
      <body>
        {children}
        <Watermark />
        <ContentGuard />
        <PwaManager />
      </body>
    </html>
  );
}
