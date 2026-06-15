from backend.rag.vector import client

client.delete_collection("rag")
print("Collection deleted")

