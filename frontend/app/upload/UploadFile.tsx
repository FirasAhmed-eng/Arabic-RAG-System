import axios from "axios";
import React, { useState } from "react";
import { Upload, FileUp } from "lucide-react";
const UploadFile = () => {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("لم يتم اختيار ملف");

  const handleSubmit = async (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();

    if (!file) {
      console.log("No file selected");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("collection_name", "rag");

    try {
      const response = await axios.post(
        "http://localhost:8000/api/upload",
        formData,
      );

      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-card border border-border rounded-xl p-6 ">
      <h1 className="text-xl font-bold mb-4 text-center">إرفع ملف</h1>
      <div className="mb-4 ">
        <input
          id="file-upload"
          type="file"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) {
              setFileName(file.name);
              setFile(file);
            }
          }}
        />

        <label
          htmlFor="file-upload"
          className="
    w-full
    flex
    items-center
    justify-center
    gap-2
    cursor-pointer
    py-2
    rounded-lg
    border
    border-border
  "
        >
          <FileUp size={18} />
          اختر ملف
        </label>
      </div>
      <button
        onClick={handleSubmit}
        className="
            cursor-pointer

    w-full
    flex
    items-center
    justify-center
    gap-2
    bg-primary
    text-primary-foreground
    py-2
    rounded-lg
  "
      >
        <Upload size={18} />
        إرفع
      </button>
    </div>
  );
};

export default UploadFile;
