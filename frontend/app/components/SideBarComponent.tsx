"use client";

import { getFiles } from "@/utils/FileList";
import { useEffect, useState } from "react";

export default function SideBarComponent() {
  const [files, setFiles] = useState<string[]>([]);

  useEffect(() => {
    getFiles().then(setFiles).catch(console.error);
  }, []);

  return (
    <aside className="w-64 min-h-screen border-r p-4">
      <h2 className="font-bold mb-4">Files</h2>

      <ul className="space-y-2">
        {files.map((file) => (
          <li key={file}>{file}</li>
        ))}
      </ul>
    </aside>
  );
}
