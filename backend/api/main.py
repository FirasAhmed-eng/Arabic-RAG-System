from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
import os
from backend.rag.ingest import process_pdf
from backend.rag.rag import rag_pipeline
from pathlib import Path
from backend.rag.ingest import preprocess_text

app = FastAPI()

allow_origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), collection_name: str = "rag"):

    file_path = os.path.join("uploads", file.filename)  # type: ignore
    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = process_pdf(file_path, collection_name)
    return {
        "filename": file.filename,
        **result,

    }


@app.get("/api/chat")
async def chat(query: str, collection_name: str = "rag"):
    query = preprocess_text(query)
    answer = rag_pipeline(query, collection_name, 10)

    return {
        "answer": answer["answer"],
        "metadata": answer["metadata"],
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/files")
async def get_files():
    data_dir = Path("data")

    files = [
        file.name
        for file in data_dir.iterdir()
        if file.is_file()
    ]

    return {"files": files}
