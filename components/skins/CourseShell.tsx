import type { ReactNode } from "react";
import { lessonBySlug } from "@/lib/lessons";
import { LessonHeader } from "@/components/lesson/header";
import { LessonNav, SkinDisclaimer } from "@/components/lesson/nav";
import { Toc } from "@/components/lesson/Toc";
import { CourseChrome } from "./CourseChrome";

/** Barcha darslar uchun umumiy qobiq: terminal sessiyasi ko'rinishidagi sahifa. */
export function CourseShell({ slug, children }: { slug: string; children: ReactNode }) {
  const lesson = lessonBySlug(slug);
  const n = String(lesson?.order ?? 1).padStart(2, "0");
  return (
    <CourseChrome slug={slug}>
      {/* Sessiya boshlanishidagi kutib olish oynasi */}
      <div className="mb-8 rounded-[var(--skin-radius)] border border-[var(--skin-accent)]/60 p-4 font-[family-name:var(--skin-mono)] text-sm">
        <div>
          <span className="text-[var(--skin-accent)]">●</span> Claude Code kursi ·{" "}
          <span className="text-[var(--skin-muted)]">dars {n}</span>
        </div>
        <div className="mt-2 text-[var(--skin-muted)]">
          cwd: ~/kurs/{slug}
        </div>
        <div className="mt-1 text-[var(--skin-muted)]">
          maqsad: tushunish → sinab ko‘rish → tekshirish
        </div>
      </div>

      <LessonHeader slug={slug} />
      <Toc />
      <article className="lesson-prose">{children}</article>
      <LessonNav slug={slug} />
      <SkinDisclaimer product="Claude Code" />
    </CourseChrome>
  );
}
