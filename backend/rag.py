from vector import get_vector_store
from llm import generate_answer


collection_name = "rag"
query = "تاريخ الذكاء الاصطناعي"


def rag_pipeline(query):
    db = get_vector_store(collection_name)

    result = db.similarity_search_with_score(
        query=query,
        k=3
    )

    context = "\n\n".join(
        [doc.page_content for doc, score in result]
    )

    return generate_answer(query, context)


answer = rag_pipeline(query)

with open("debug_output.txt", "w", encoding="utf-8") as f:
    f.write(answer)  # type: ignore
