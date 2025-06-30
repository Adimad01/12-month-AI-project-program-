import { Dialog } from "@headlessui/react";
import { useState } from "react";

export default function PreviewModal({
  file,
  onClose,
  onConfirm,
}: {
  file: File;
  onClose: () => void;
  onConfirm: (file: File) => void;
}) {
  const [open, setOpen] = useState(true);
  const close = () => {
    setOpen(false);
    onClose();
  };

  return (
    <Dialog
      open={open}
      onClose={close}
      className="fixed inset-0 z-50 flex items-center justify-center"
    >
      <Dialog.Overlay className="fixed inset-0 bg-black/30" />
      <div className="relative bg-white rounded p-4 max-w-lg w-full">
        <Dialog.Title className="text-lg font-medium">
          Preview Photo
        </Dialog.Title>

        <img
          src={URL.createObjectURL(file)}
          alt="preview"
          className="w-full object-contain mt-3 max-h-96"
        />

        <div className="mt-4 flex justify-end space-x-2">
          <button className="px-3 py-1 border rounded" onClick={close}>
            Cancel
          </button>
          <button
            className="px-3 py-1 border rounded"
            onClick={() => {
              setOpen(false);
              onConfirm(file);
            }}
          >
            Use Photo
          </button>
        </div>
      </div>
    </Dialog>
  );
}
