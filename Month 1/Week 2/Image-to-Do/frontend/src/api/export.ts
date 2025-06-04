export async function exportTasks(
  provider: "todoist" | "google",
  tasks: any[]
): Promise<void> {
  const res = await fetch(`${import.meta.env.VITE_API}/export`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ provider, tasks }),
  });
  if (!res.ok) throw new Error("Export failed");
}
