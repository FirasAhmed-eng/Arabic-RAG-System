from qdrant_client.models import Distance, VectorParams
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
    prefer_grpc=False,
)


def vector_embedding(docs, collection_name):
    print("Creating embeddings...")
    if not client.collection_exists(collection_name):

        dim = len(embeddings.embed_query("test"))

        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=dim,
                distance=Distance.COSINE,
            ),
        )

    db = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )

    BATCH_SIZE = 100

    for i in range(0, len(docs), BATCH_SIZE):

        batch = docs[i:i + BATCH_SIZE]

        print(
            f"Uploading batch "
            f"{i//BATCH_SIZE + 1}"
        )
        print("Uploading to Qdrant...")
        db.add_documents(batch)
    # db.add_documents(docs)

    return db


def get_vector_store(collection_name):
    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )
