from ingest import extract_text
from chunking import chunk_text
from vector import vector_embedding

collection_name = "rag"

raw_text = extract_text("data/SDAIA.pdf")
chunks = chunk_text(raw_text)
db = vector_embedding(chunks, collection_name)

result = db.similarity_search(query="Alan Turing ", k=1)

with open("debug_output.txt", "w", encoding="utf-8") as f:

    for doc in result:
        f.write(f"{doc.page_content} \n\n Metadata: {doc.metadata}")
        print(f"{doc.page_content} Metadata: {doc.metadata}")
