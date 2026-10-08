"use client";

import { useRef, useState, type ComponentProps } from "react";

/** Kod bloki + "Nusxa" tugmasi. MDX dagi har bir ``` blok shu orqali chiqadi. */
export function CopyPre(props: ComponentProps<"pre">) {
  const ref = useRef<HTMLPreElement>(null);
  const [done, setDone] = useState(false);

  const copy = async () => {
    const text = ref.current?.innerText.replace(/\n$/, "") ?? "";
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      // Eski brauzerlar yoki ruxsat yo'q: matnni belgilab qo'yamiz
      const sel = window.getSelection();
      const range = document.createRange();
      if (ref.current && sel) {
        range.selectNodeContents(ref.current);
        sel.removeAllRanges();
        sel.addRange(range);
      }
      return;
    }
    setDone(true);
    setTimeout(() => setDone(false), 1500);
  };

  return (
    <div className="group relative">
      <pre ref={ref} {...props} />
      <button
        type="button"
        onClick={copy}
        aria-label="Kodni nusxalash"
        className="absolute top-2 right-2 rounded border border-[var(--skin-border)] bg-[var(--skin-surface)] px-2 py-0.5 font-[family-name:var(--skin-mono)] text-[11px] text-[var(--skin-muted)] opacity-80 transition-opacity hover:text-[var(--skin-text)] hover:opacity-100"
      >
        {done ? "nusxalandi ✓" : "nusxa"}
      </button>
    </div>
  );
}
