from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
import os
from backend.rag.ingest import process_pdf

app = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = os.path.join("data", file.filename)  # type: ignore
    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = process_pdf(file_path)
    return {
        "filename": file.filename,
        **result
    }


@app.post("/chat")
async def chat():
    return {"message": "chat response sent successfully"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
