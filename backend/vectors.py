from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os
load_dotenv()


url = os.getenv("QDRANT_ENDPOINT")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def vector_embedding(docs, collection_name) -> QdrantVectorStore:
    qdrant = QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        url=url,
        prefer_grpc=True,
        collection_name=collection_name
    )
    return qdrant
