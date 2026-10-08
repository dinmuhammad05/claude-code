"use client";

import { useEffect, useState } from "react";

/**
 * O'qish sozlamalari: matn o'lchami va mavzu (tizimga mos / yorug' / qorong'i).
 * Tanlov <html data-fs data-theme> ga yoziladi va brauzerda eslab qolinadi.
 * Sahifa chizilishidan oldingi qo'llash — layout.tsx dagi PREFS_SCRIPT.
 */
const SIZES = ["s", "m", "l", "xl"] as const;
type Size = (typeof SIZES)[number];
type Theme = "auto" | "light" | "dark";

function read<T extends string>(key: string, fallback: T): T {
  try {
    return (localStorage.getItem(key) as T) || fallback;
  } catch {
    return fallback;
  }
}
function save(key: string, value: string) {
  try {
    localStorage.setItem(key, value);
  } catch {
    // Saqlash imkoni yo'q (yashirin rejim) — faqat shu sahifada amal qiladi
  }
}

export function ReadingPrefs() {
  const [size, setSize] = useState<Size>("m");
  const [theme, setTheme] = useState<Theme>("auto");

  useEffect(() => {
    setSize(read<Size>("cckurs:fs", "m"));
    setTheme(read<Theme>("cckurs:theme", "auto"));
  }, []);

  const applySize = (s: Size) => {
    setSize(s);
    save("cckurs:fs", s);
    if (s === "m") delete document.documentElement.dataset.fs;
    else document.documentElement.dataset.fs = s;
  };
  const applyTheme = (t: Theme) => {
    setTheme(t);
    save("cckurs:theme", t);
    if (t === "auto") delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = t;
  };

  const i = SIZES.indexOf(size);
  const nextTheme: Theme = theme === "auto" ? "light" : theme === "light" ? "dark" : "auto";
  const themeLabel = { auto: "Mavzu: tizimga mos", light: "Mavzu: yorug‘", dark: "Mavzu: qorong‘i" }[theme];

  const btn =
    "flex h-8 min-w-8 items-center justify-center rounded px-1.5 text-xs font-semibold text-[var(--skin-text)] hover:bg-[var(--skin-surface-2)] disabled:opacity-35";

  return (
    <div className="flex items-center rounded border border-[var(--skin-border)]" role="group" aria-label="O‘qish sozlamalari">
      <button
        type="button"
        className={btn}
        onClick={() => applySize(SIZES[i - 1])}
        disabled={i <= 0}
        aria-label="Matnni kichraytirish"
        title="Matnni kichraytirish"
      >
        A−
      </button>
      <button
        type="button"
        className={btn}
        onClick={() => applySize(SIZES[i + 1])}
        disabled={i >= SIZES.length - 1}
        aria-label="Matnni kattalashtirish"
        title="Matnni kattalashtirish"
      >
        A+
      </button>
      <button
        type="button"
        className={btn}
        onClick={() => applyTheme(nextTheme)}
        aria-label={`${themeLabel}. Almashtirish`}
        title={themeLabel}
      >
        {theme === "light" ? <Sun /> : theme === "dark" ? <Moon /> : <Auto />}
      </button>
    </div>
  );
}

/** <head> dagi skript: saqlangan tanlovni birinchi chizilishdan oldin qo'llaydi (miltillamaslik uchun). */
export const PREFS_SCRIPT = `try{var d=document.documentElement,f=localStorage.getItem("cckurs:fs"),t=localStorage.getItem("cckurs:theme");if(f&&f!=="m")d.dataset.fs=f;if(t==="light"||t==="dark")d.dataset.theme=t}catch(e){}`;

function Sun() {
  return (
    <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" aria-hidden>
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
    </svg>
  );
}
function Moon() {
  return (
    <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z" />
    </svg>
  );
}
function Auto() {
  return (
    <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden>
      <circle cx="12" cy="12" r="8" />
      <path d="M12 4a8 8 0 0 1 0 16Z" fill="currentColor" />
    </svg>
  );
}
