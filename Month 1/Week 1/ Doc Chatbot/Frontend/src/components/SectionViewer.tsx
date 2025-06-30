// ------------------------------
// src/components/SectionViewer.tsx  (state‑safe & summary button)
// ------------------------------
import { useState, useEffect } from "react";
import { summarize } from "@/lib/api";
import { Button } from "@/components/ui/button";

interface Props {
  workspaceId: string;
  sections: string[]; // simple list of section titles
}

export default function SectionViewer({ workspaceId, sections }: Props) {
  const [active, setActive] = useState<string | null>(null);
  const [summary, setSummary] = useState<string>("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!active) return;
    (async () => {
      setLoading(true);
      try {
        const text = await summarize(workspaceId, active);
        setSummary(text);
      } catch (e) {
        console.error(e);
        setSummary("Failed to summarize.");
      } finally {
        setLoading(false);
      }
    })();
  }, [active, workspaceId]);

  if (!sections?.length) return null;

  return (
    <div className="h-full flex">
      {/* left list */}
      <div className="w-56 border-r overflow-y-auto bg-muted/30">
        {sections.map((title) => (
          <Button
            key={title}
            variant={active === title ? "secondary" : "ghost"}
            className="w-full justify-start rounded-none"
            onClick={() => setActive(title)}
          >
            {title}
          </Button>
        ))}
      </div>

      {/* right pane */}
      <div className="flex-1 p-4 overflow-y-auto">
        {active ? (
          loading ? (
            <p className="text-muted-foreground">Loading summary…</p>
          ) : (
            <pre className="whitespace-pre-wrap font-sans leading-relaxed">{summary}</pre>
          )
        ) : (
          <p className="text-muted-foreground">Select a section to see the summary.</p>
        )}
      </div>
    </div>
  );
}
