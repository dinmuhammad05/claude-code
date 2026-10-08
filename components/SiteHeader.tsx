import Link from "next/link";
import { site } from "@/lib/site";
import { AuthorPhoto } from "@/components/AuthorPhoto";
import { ReadingPrefs } from "@/components/ReadingPrefs";

/** Bosh sahifa va kurs rejasi uchun yuqori panel: loyiha nomi va muallif. */
export function SiteHeader() {
  return (
    <header className="sticky top-0 z-30 border-b border-[var(--skin-border)] bg-[var(--skin-bg)]/85 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center gap-3 px-5 py-3">
        <Link href="/" className="flex min-w-0 items-center gap-2.5">
          <Mark className="h-7 w-7 shrink-0" />
          <span className="truncate font-semibold">
            <span className="hidden sm:inline">Claude Code kursi</span>
            <span className="sm:hidden">Claude Code</span>
          </span>
        </Link>

        {/* Muallif */}
        <div className="ml-auto flex items-center gap-2">
          <ReadingPrefs />
          <span className="hidden text-xs text-[var(--skin-muted)] sm:inline">muallif</span>
          <a
            href={site.author.portfolio}
            target="_blank"
            rel="noopener noreferrer"
            title="Muallif portfoliosi"
            className="flex items-center gap-2 rounded-full border border-[var(--skin-border)] py-1 pr-3 pl-1 transition-colors hover:bg-[var(--skin-surface)]"
          >
            <span
              aria-hidden
              className="flex overflow-hidden h-7 w-7 items-center justify-center rounded-full bg-[var(--skin-surface-2)] font-[family-name:var(--skin-mono)] text-[11px] font-bold text-[var(--skin-accent)]"
            >
              <AuthorPhoto className="h-full w-full" fallback="dM" />
            </span>
            <span className="text-sm font-medium">{site.author.handle}</span>
          </a>
          <a
            href={site.author.telegramUrl}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={`Telegram ${site.author.telegram}`}
            title={`Telegram ${site.author.telegram}`}
            className="flex h-9 w-9 items-center justify-center rounded-full border border-[var(--skin-border)] transition-colors hover:bg-[var(--skin-surface)]"
          >
            <TelegramIcon className="h-[18px] w-[18px]" />
          </a>
        </div>
      </div>
    </header>
  );
}

function Mark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" aria-hidden>
      <rect x="2.5" y="4" width="19" height="16" rx="3" stroke="var(--skin-accent)" strokeWidth="1.7" />
      <path
        d="m7 9.5 3 2.5-3 2.5M12.5 15h4.5"
        stroke="var(--skin-accent)"
        strokeWidth="1.7"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function TelegramIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="currentColor" aria-hidden>
      <path d="M21.7 3.5 2.9 10.8c-1.1.4-1.1 1.1-.2 1.4l4.7 1.5 1.8 5.5c.2.6.4.8.8.8.4 0 .6-.2.9-.5l2.2-2.1 4.6 3.4c.8.5 1.4.2 1.6-.8l3-14c.3-1.2-.5-1.8-1.6-1.5ZM7.6 13.3l9.8-6.2c.5-.3.9-.1.5.2l-8.4 7.6-.3 3.5-1.6-5.1Z" />
    </svg>
  );
}
