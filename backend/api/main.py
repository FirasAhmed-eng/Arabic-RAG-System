from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
import os
from backend.rag.ingest import process_pdf
from backend.rag.rag import rag_pipeline
app = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), collection_name: str = "rag"):

    file_path = os.path.join("data", file.filename)  # type: ignore
    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = process_pdf(file_path, collection_name)
    return {
        "filename": file.filename,
        **result
    }


@app.get("/chat")
async def chat(query: str):
    answer = rag_pipeline(query)
    return answer


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
