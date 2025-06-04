// ------------------------------
// src/lib/api.ts  (stream helpers + summarize export)
// ------------------------------
export async function* chat(
  workspaceId: string,
  question: string,
): AsyncGenerator<string> {
  const res = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ workspace_id: workspaceId, question }),
  });

  if (!res.ok || !res.body) {
    throw new Error(`Chat error (${res.status})`);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    let idx: number;
    while ((idx = buffer.indexOf("\n\n")) !== -1) {
      const raw = buffer.slice(0, idx).trim();
      buffer = buffer.slice(idx + 2);
      if (raw.startsWith("data:")) {
        yield raw.slice(5).trimStart();
      }
    }
  }
}

export interface UploadResponse {
  workspace_id: string;
}

export async function uploadFile(file: File): Promise<UploadResponse> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("http://127.0.0.1:8000/upload", {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error(`Upload failed (${res.status})`);
  return res.json();
}

export async function summarize(
  workspaceId: string,
  sectionTitle = "",
): Promise<string> {
  const res = await fetch("http://127.0.0.1:8000/summarize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ workspace_id: workspaceId, section_title: sectionTitle }),
  });
  if (!res.ok) throw new Error(`Summary error (${res.status})`);
  const data = await res.json();
  return data.summary ?? "";
}