from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
import os
from backend.rag.ingest import process_pdf
from backend.rag.rag import rag_pipeline
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), collection_name: str = "rag"):

    file_path = os.path.join("data", file.filename)  # type: ignore
    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = process_pdf(file_path, collection_name)
    return {
        "filename": file.filename,
        **result,

    }


@app.get("/api/chat")
async def chat(query: str, collection_name: str = "rag"):
    answer = rag_pipeline(query, collection_name, 6)

    return {
        "answer": answer["answer"],
        "metadata": answer["metadata"],
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
