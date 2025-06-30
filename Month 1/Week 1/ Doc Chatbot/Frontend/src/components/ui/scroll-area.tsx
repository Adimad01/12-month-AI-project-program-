// ──────────────────────────────────────────────────────────
// src/components/ui/scroll-area.tsx
// ──────────────────────────────────────────────────────────
import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "react";

export function ScrollArea({ className, ...rest }: HTMLAttributes<HTMLDivElement>) {
  return <div {...rest} className={cn("overflow-y-auto", className)} />;
}
