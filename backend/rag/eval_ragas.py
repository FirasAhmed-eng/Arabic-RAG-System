from datasets import Dataset
from dotenv import load_dotenv
from openai import OpenAI

from ragas import evaluate
from ragas.llms import llm_factory
from ragas.metrics import Faithfulness

from backend.rag.llm import generate_answer
from backend.rag.vector import get_vector_store

import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

llm = llm_factory(
    "gpt-4.1-mini",
    provider="openai",
    client=client,
)

faithfulness_metric = Faithfulness(llm=llm)

TEST_SET = [
    {
        "question": "تاريخ الذكاء الاصطناعي",
        "reference": (
            "بدأ الذكاء الاصطناعي في أوائل أربعينيات القرن الماضي "
            "حين اقترح بعض العلماء نموذجًا للخلايا العصبية الاصطناعية، "
            "وبرز مفهوم الذكاء الاصطناعي بشكل كبير في بداية الخمسينيات."
        ),
    },
    {
        "question": "مجالات الذكاء الاصطناعي",
        "reference": (
            "مجالات الذكاء الاصطناعي تشمل عمل تنبؤات، "
            "وتوليد محتوى، وتقديم توصيات، واتخاذ قرارات."
        ),
    },
]


def run_rag(query: str, collection_name: str = "rag", top_k: int = 10):
    db = get_vector_store(collection_name)

    results = db.similarity_search_with_score(
        query=query,
        k=top_k,
    )

    contexts = [
        doc.page_content
        for doc, _ in results
    ]

    context_text = "\n\n".join(contexts)

    answer = generate_answer(
        query=query,
        context=context_text,
    )

    return answer, contexts


def build_evaluation_dataset(
    test_set: list[dict],
    collection_name: str = "rag",
):
    rows = []

    for sample in test_set:
        question = sample["question"]

        print(f"Evaluating: {question}")

        answer, contexts = run_rag(
            query=question,
            collection_name=collection_name,
        )

        rows.append(
            {
                "user_input": question,
                "response": answer,
                "retrieved_contexts": contexts,
                "reference": sample["reference"],
            }
        )

    return Dataset.from_list(rows)


def evaluate_rag():
    dataset = build_evaluation_dataset(TEST_SET)

    result = evaluate(
        dataset=dataset,
        metrics=[faithfulness_metric],
    )

    print("\n=== OVERALL RESULTS ===")
    print(result)

    df = result.to_pandas() # type: ignore

    print("\n=== PER QUESTION RESULTS ===")
    print(df)

    df.to_csv("evaluation_results.csv", index=False)

    return result


if __name__ == "__main__":
    evaluate_rag()