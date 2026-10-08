import type { Metadata } from "next";
import { CourseShell } from "@/components/skins/CourseShell";
import { lessonMetadata } from "@/lib/seo";

export const metadata: Metadata = lessonMetadata("ornatish");

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div data-skin="cc" className="min-h-screen bg-[var(--skin-bg)] text-[var(--skin-text)]">
      <CourseShell slug="ornatish">{children}</CourseShell>
    </div>
  );
}
