
import axios from "axios";
import React, { useState } from "react";

const Upload = () => {
  const [file, setFile] = useState<File | null>(null);

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
    <div>
      <input
        type="file"
        onChange={(e) => {
          if (e.target.files?.[0]) {
            setFile(e.target.files[0]);
          }
        }}
      />

      <button onClick={handleSubmit}>Upload</button>
    </div>
  );
};

export default Upload;
