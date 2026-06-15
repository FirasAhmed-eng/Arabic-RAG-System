from backend.rag.vector import get_vector_store
from backend.rag.llm import generate_answer


def rag_pipeline(query, collection_name="rag", top_k=10):
    db = get_vector_store(collection_name)

    result = db.similarity_search_with_score(
        query=query,
        k=top_k
    )

    print("\n=== RESULTS ===")
    for i, (doc, score) in enumerate(result):
        print("\n---")
        print("Rank:", i)
        print("Score:", score)
        print("Chunk ID:", doc.metadata["chunk_id"])
        print("Page:", doc.metadata["page"])
        print(doc.page_content[:100])

    context = "\n\n".join(
        [doc.page_content for doc, score in result]
    )
    with open("context.txt", "w") as f:
        f.write(context)
    answer = generate_answer(query, context)
    contexts = [doc.page_content for doc, score in result]

    print("Retrieved:", len(contexts))
    print("Unique:", len(set(contexts)))
    return {
        "answer": answer,
        "metadata": [doc.metadata for doc, score in result]
    }
