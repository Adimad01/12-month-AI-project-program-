import { useState } from "react";
import ImageCapture from "./components/ImageCapture";
import PreviewModal from "./components/PreviewModal";
import TaskList from "./components/TaskList";
import { ocr } from "./api/ocr";
import { taskify } from "./api/taskify";
import { exportTasks } from "./api/export";

export interface Task {
  text: string;
  assignee?: string;
  due?: string;
  tags?: string[];
}

export default function App() {
  const [rawPhoto, setRawPhoto] = useState<File | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleProcess(photo: File) {
    setLoading(true);
    try {
      const lines = await ocr(photo);
      const { tasks } = await taskify({ lines });
      setTasks(tasks);
    } catch (err) {
      console.error(err);
      alert("Failed to process image");
    } finally {
      setLoading(false);
    }
  }

  function handleExport(provider: "todoist" | "google") {
    exportTasks(provider, tasks).catch((err) => {
      console.error(err);
      alert("Export failed");
    });
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-6">Image‑to‑Do</h1>

      {/* 1. Capture or upload a photo */}
      <ImageCapture onDone={(file) => setRawPhoto(file)} />

      {/* 2. Optional preview modal */}
      {rawPhoto && (
        <PreviewModal
          file={rawPhoto}
          onClose={() => setRawPhoto(null)}
          onConfirm={(file) => {
            handleProcess(file);
            setRawPhoto(null);
          }}
        />
      )}

      {/* 3. Loading indicator */}
      {loading && <p className="mt-4 text-gray-600">Processing…</p>}

      {/* 4. Render extracted tasks */}
      <TaskList tasks={tasks} />

      {/* 5. Export buttons */}
      {tasks.length > 0 && (
        <div className="mt-6 space-x-4">
          <button
            className="rounded border px-3 py-1"
            onClick={() => handleExport("todoist")}
          >
            Export → Todoist
          </button>
          <button
            className="rounded border px-3 py-1"
            onClick={() => handleExport("google")}
          >
            Export → Google Tasks
          </button>
        </div>
      )}
    </div>
  );
}
