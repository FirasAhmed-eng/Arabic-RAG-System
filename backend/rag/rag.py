from backend.rag.vector import get_vector_store
from backend.rag.llm import generate_answer


def rag_pipeline(query, collection_name="rag", top_k: int = 3):
    db = get_vector_store(collection_name)

    result = db.similarity_search_with_score(
        query=query,
        k=top_k
    )

    context = "\n\n".join(
        [doc.page_content for doc, score in result if score > 0.5]
    )

    answer = generate_answer(query, context)
    metadata = [doc.metadata for doc, score in result if score > 0.5]
    return {"answer": answer, "metadata": metadata}
