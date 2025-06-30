import { useRef } from "react";

export default function ImageCapture({
  onDone,
}: {
  onDone: (file: File) => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <div className="space-y-4">
      <button
        onClick={() => inputRef.current?.click()}
        className="rounded-xl border px-4 py-2"
      >
        Take / Upload Photo
      </button>

      <input
        ref={inputRef}
        hidden
        type="file"
        accept="image/*"
        capture="environment"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) onDone(file);
        }}
      />
    </div>
  );
}
