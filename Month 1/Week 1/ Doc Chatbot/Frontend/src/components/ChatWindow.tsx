// ------------------------------
// src/components/ChatWindow.tsx  (fixed streaming logic & ui polish)
// ------------------------------
import { useState, useRef, FormEvent } from "react";
import { chat } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { CornerDownLeft, Loader2 } from "lucide-react";

type Message = { role: "user" | "assistant"; content: string };

interface Props {
  workspaceId: string;
  messages: Message[];
  onNewMessage(msg: Message): void;
}

export default function ChatWindow({ workspaceId, messages, onNewMessage }: Props) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  async function send(e: FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;

    const question = input.trim();
    onNewMessage({ role: "user", content: question });
    setInput("");
    setLoading(true);

    let answer = "";
    try {
      for await (const chunk of chat(workspaceId, question)) {
        answer += chunk;
        // stream‑update last assistant message
        onNewMessage({ role: "assistant", content: answer });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
      // auto‑scroll
      queueMicrotask(() => {
        containerRef.current?.scrollTo({ top: containerRef.current.scrollHeight });
      });
    }
  }

  return (
    <div className="flex flex-col h-full border rounded-lg overflow-hidden">
      <div ref={containerRef} className="flex-1 space-y-4 p-4 overflow-y-auto bg-muted/40">
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
            <div
              className={
                m.role === "user"
                  ? "inline-block max-w-[75%] rounded-lg bg-primary text-primary-foreground px-3 py-2"
                  : "inline-block max-w-[75%] rounded-lg bg-background border px-3 py-2"
              }
            >
              {m.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="text-left">
            <div className="inline-flex items-center space-x-2 rounded-lg border px-3 py-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Thinking…</span>
            </div>
          </div>
        )}
      </div>

      <form onSubmit={send} className="flex gap-2 border-t bg-background p-3">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something…"
          className="flex-1"
        />
        <Button type="submit" disabled={!input.trim() || loading} className="shrink-0">
          <CornerDownLeft className="h-4 w-4" />
        </Button>
      </form>
    </div>
  );
}
