// ------------------------------
// src/components/UploadZone.tsx  (minor: color & reset)
// ------------------------------
import { useState } from "react";
import { uploadFile, UploadResponse } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { FileUp, Check, Loader2 } from "lucide-react";

interface Props {
  onReady(resp: UploadResponse): void;
}

export default function UploadZone({ onReady }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [done, setDone] = useState(false);

  async function handleUpload() {
    if (!file) return;
    setUploading(true);
    try {
      const resp = await uploadFile(file);
      setDone(true);
      onReady(resp);
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="border-2 border-dashed border-muted rounded-lg p-6 text-center space-y-4">
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => {
          setFile(e.target.files?.[0] ?? null);
          setDone(false);
        }}
        className="hidden"
        id="file-input"
      />
      <label htmlFor="file-input" className="cursor-pointer">
        <FileUp className="mx-auto h-8 w-8 text-muted-foreground" />
        <p className="mt-2 text-sm text-muted-foreground">Click to choose a PDF</p>
      </label>
      <Button onClick={handleUpload} disabled={!file || uploading || done} className="w-full">
        {uploading ? <Loader2 className="h-4 w-4 animate-spin" /> : done ? <Check className="h-4 w-4" /> : "Upload"}
      </Button>
    </div>
  );
}