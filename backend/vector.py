from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os
load_dotenv()


url = os.getenv("QDRANT_ENDPOINT")
qdrant_api = os.getenv("QDRANT_API_KEY")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


def vector_embedding(docs, collection_name) -> QdrantVectorStore:
    qdrant = QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        url=url,
        prefer_grpc=True,
        collection_name=collection_name,
        api_key=qdrant_api,
        force_recreate=True
    )
    return qdrant
