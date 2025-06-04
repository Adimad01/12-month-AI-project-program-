// src/components/TaskList.tsx
import type { Task } from "../App";   // 👈 add `type`

export default function TaskList({ tasks }: { tasks: Task[] }) {
  if (tasks.length === 0) return null;

  return (
    <ul className="mt-6 space-y-2">
      {tasks.map((t, idx) => (
        <li key={idx} className="p-3 border rounded flex flex-col">
          <span>{t.text}</span>
          {t.due && (
            <span className="text-sm text-gray-500">
              Due: {new Date(t.due).toLocaleDateString()}
            </span>
          )}
        </li>
      ))}
    </ul>
  );
}
