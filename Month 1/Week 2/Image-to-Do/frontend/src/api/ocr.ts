export async function ocr(file: File): Promise<string[]> {
  const form = new FormData();
  form.append("img", file);
  const res = await fetch(`${import.meta.env.VITE_API}/ocr`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error("OCR failed");
  return (await res.json()).text;
}
