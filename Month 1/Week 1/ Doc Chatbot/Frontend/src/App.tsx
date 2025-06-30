// ------------------------------
// src/App.tsx  (wire‑up layout)
// ------------------------------
import { useState } from "react";
import UploadZone from "@/components/UploadZone";
import ChatWindow from "@/components/ChatWindow";
import SectionViewer from "@/components/SectionViewer";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function App() {
  const [workspace, setWorkspace] = useState<string | null>(null);
  const [sections, setSections] = useState<string[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);

  return (
    <div className="flex h-screen divide-x">
      <div className="w-80 p-4">
        {!workspace ? (
          <UploadZone
            onReady={(resp) => {
              setWorkspace(resp.workspace_id);
              // placeholder — fetch TOC if you have an endpoint; else leave empty
              setSections(["Introduction", "Methods", "Results", "Conclusion"]);
            }}
          />
        ) : (
          <SectionViewer workspaceId={workspace} sections={sections} />
        )}
      </div>

      {workspace && (
        <div className="flex-1 flex flex-col">
          <ChatWindow
            workspaceId={workspace}
            messages={messages}
            onNewMessage={(m) =>
              setMessages((prev) => {
                const next = [...prev];
                // if last is assistant & streaming, replace it
                if (m.role === "assistant" && next[next.length - 1]?.role === "assistant") {
                  next[next.length - 1] = m;
                  return [...next];
                }
                return [...next, m];
              })
            }
          />
        </div>
      )}
    </div>
  );
}
