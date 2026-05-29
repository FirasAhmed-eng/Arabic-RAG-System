from ingest import extract_text
from chunking import chunk_text
from vector import vector_embedding
from llm import generate_answer


collection_name = "rag"


query = "ماهو الذكاء الاصطناعي؟"


def rag_pipeline(query):
    raw_text = extract_text("data/SDAIA.pdf")
    chunks = chunk_text(raw_text)
    print(len(chunks))
    db = vector_embedding(chunks, collection_name)

    result = db.similarity_search_with_score(query=query, k=3)

    context = "\n\n".join([doc.page_content for doc, score in result])

    answer = generate_answer(query, context)

    return answer


answer = rag_pipeline(query)

with open("debug_output.txt", "w", encoding="utf-8") as f:
    f.write(answer)  # type: ignore
