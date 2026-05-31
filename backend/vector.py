from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os
from qdrant_client import QdrantClient

load_dotenv()


url = os.getenv("QDRANT_ENDPOINT")
qdrant_api = os.getenv("QDRANT_API_KEY")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

client = QdrantClient(
    url=url,
    api_key=qdrant_api,
    prefer_grpc=True,
)


def vector_embedding(docs, collection_name):
    if not client.collection_exists(collection_name):
        return QdrantVectorStore.from_documents(
            documents=docs,
            embedding=embeddings,
            client=client,
            collection_name=collection_name,
        )

    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )


def get_vector_store(collection_name):
    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )
