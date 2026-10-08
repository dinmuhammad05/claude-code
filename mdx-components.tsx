import type { MDXComponents } from "mdx/types";
import * as Lesson from "@/components/lesson";
import { CopyPre } from "@/components/lesson/CopyPre";

/**
 * MDX ichida import qilmasdan ishlatiladigan komponentlar.
 * Har bir dars .mdx faylida <Step>, <Arch>, <QA> ... to'g'ridan-to'g'ri yoziladi.
 * Kod bloklari (pre) "Nusxa" tugmasi bilan chiqadi.
 */
export function useMDXComponents(components: MDXComponents): MDXComponents {
  return { ...Lesson, pre: CopyPre, ...components };
}
