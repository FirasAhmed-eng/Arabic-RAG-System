from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os
from qdrant_client import QdrantClient

load_dotenv()


url = os.getenv("QDRANT_ENDPOINT")
qdrant_api = os.getenv("QDRANT_API_KEY")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


def vector_embedding(docs, collection_name):
    client = QdrantClient(
        url=url,
        api_key=qdrant_api,
        prefer_grpc=True,
    )

    if not client.collection_exists(collection_name):
        db = QdrantVectorStore.from_documents(
            documents=docs,
            embedding=embeddings,
            url=url,
            api_key=qdrant_api,
            prefer_grpc=True,
            collection_name=collection_name,
        )
    else:
        db = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings,
        )

    return db
