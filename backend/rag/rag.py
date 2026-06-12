from backend.rag.vector import get_vector_store
from backend.rag.llm import generate_answer


def rag_pipeline(query, collection_name="rag", top_k=10):
    db = get_vector_store(collection_name)

    result = db.similarity_search_with_score(
        query=query,
        k=top_k
    )

    print("\n=== RESULTS ===")
    for doc, score in result:
        print(score)

    context = "\n\n".join(
        [doc.page_content for doc, score in result]
    )

    return {
        "answer": generate_answer(query, context),
        "metadata": [doc.metadata for doc, score in result]
    }
