from langchain_text_splitters import RecursiveCharacterTextSplitter
from ingest import extract_text
from langchain_core.documents import Document


def chunk_text(pages, chunk_size=500, chunk_overlap=50) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "؟", ".", "،", " ", ""])

    documents = []

    for page_data in pages:
        page_num = page_data["page"]
        text = page_data["text"]
        source = page_data["source"]

        chunks = splitter.split_text(text)
        for chunk_index, chunk in enumerate(chunks):
            chunk_id = f"{source}_p{page_num}_c{chunk_index}"

            doc = Document(
                page_content=chunk,
                metadata={
                    "source": source,
                    "page": page_num,
                    "chunk_id": chunk_id,
                    "language": "ar"

                },
            )
            documents.append(doc)
    return documents


# --------- Enable comments for debugging ---------

# pages = extract_text("data/SDAIA.pdf")

# documents = chunk_text(pages)

# print(documents[0].page_content)
# print(documents[0].metadata)
# print(f"Total chunks: {len(documents)}")

# with open("Chunked.txt", "w", encoding="utf-8") as f:
#     for chunk in documents:
#         chunk = chunk.page_content + "\n\n"
#         f.write(chunk)
# #  print(chunked_text)
