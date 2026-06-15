
from qdrant_client.models import Distance, VectorParams
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os
from qdrant_client import QdrantClient
import uuid

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

client = QdrantClient(
    url=os.getenv("QDRANT_ENDPOINT"),
    api_key=os.getenv("QDRANT_API_KEY"),
    prefer_grpc=False,
)


def _create_collection_if_needed(collection_name: str):
    if client.collection_exists(collection_name):
        return

    dim = len(embeddings.embed_query("test"))

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=dim,
            distance=Distance.COSINE,
        ),
    )


def vector_embedding(docs, collection_name: str):
    _create_collection_if_needed(collection_name)

    db = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )

    batch_size = 100

    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]

        ids = [
            str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.metadata["chunk_id"]))
            for doc in batch
        ]

        print(
            f"Uploading batch {i // batch_size + 1}"
        )

        db.add_documents(
            documents=batch,
            ids=ids,
        )

    info = client.get_collection(collection_name)

    print(
        f"Collection points: "
        f"{info.points_count}"
    )

    return db


def get_vector_store(collection_name: str):
    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )
