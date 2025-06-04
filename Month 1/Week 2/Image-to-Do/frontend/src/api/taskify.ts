export async function taskify(payload: { lines: string[] }): Promise<{
  tasks: any[];
}> {
  const res = await fetch(`${import.meta.env.VITE_API}/taskify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Taskify failed");
  return await res.json();
}
