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
        "question": "ماهو تاريخ الذكاء الاصطناعي",
        "reference": (
            "بدأ الذكاء الاصطناعي في أوائل أربعينيات القرن الماضي "
            "حين اقترح بعض العلماء نموذجًا للخلايا العصبية الاصطناعية، "
            "وبرز مفهوم الذكاء الاصطناعي بشكل كبير في بداية الخمسينيات."
        ),
    },
    {
        "question":  " ماهي مجالات الذكاء الاصطناعي",
        "reference": (
            "مجالات الذكاء الاصطناعي تشمل عمل تنبؤات، "
            "وتوليد محتوى، وتقديم توصيات، واتخاذ قرارات."
        ),
    },
    {
        "question": "ماهي أمثلة الذكاء الاصطناعي؟",
        "reference": (
            "الحكومة, التعليم, الصحة, الطاقة, النقل والمواصلات, الصناعة, المال, التسويق, الزراعة"
        ),
    },
    {
        "question": "ممن يتكون فريق الذكاء الاصطناعي؟",
        "reference": (
            """
            العمــل فــي مشــاريع الــذكاء الاصطناعــي يتطلــب الدمــج بيــن المختصيــن فــي مجــال الأعمــال مــع المختصيــن فــي مجــال الــذكاء الاصطناعــي وتقنيــة المعلومــات، وتختلــف الأدوار المطلوبــة بحســب طبيعــة المشــروع وحجمــه، ومــن أشــهر هــذه الأدوار:
            عالم بيانات
            فهم المتطلبات، وهندسة البيانات، وبناء النماذج واختبارها.
            مهندس تعلم آلة
            هندسة البيانات، وبناء النماذج وتطبيقها.
            محلل بيانات
            تحليل البيانات وتصميم لوحات المعلومات والتقارير.
            مهندس بيانات
            هندسة البيانات وتجهيز البيئة التشغيلية.
            مهندس برمجيات
            تطوير البرمجيات وتصميم الواجهات وقواعد البيانات.
            محلل أعمال
            شرح المتطلبات وتحديد الأولويات والمستهدفات.
            مدير مشاريع
            إدارة المشاريع ومتابعة المهام.
            """
        ),
    },
    {
        "question": "ماهي عوامل النجاح الذكاء الاصطناعي؟",
        "reference": """
    مواءمة مبادرات الذكاء الاصطناعي مع أولويات الأعمال.
    توفير نظرة شاملة عن البيانات.
    تعيين أساسيات حوكمة البيانات.
    توضيح الأدوار والمسؤوليات.
    """,
    },
    {
        "question": "ماهي التحديات والمخاطر للذكاء الاصطناعي؟",
        "reference": """
    عدم وضوح المشكلة.
    نقص البيانات.
    سهولة المشكلة.
    البيانات غير المنظمة.
    """,
    },
    {
        "question": "ما تأثير الذكاء الاصطناعي على الوظائف؟",
        "reference": (
            "لا شــك أن الــذكاء الاصطناعــي ســيؤثر فــي كثيــر مــن الوظائــف الموجــودة اليــوم، وخاصــة الأعمــال الروتينيــة والبســيطة، ولكــن مــن المتوقــع أن يخلــق الــذكاء الاصطناعــي المزيــد مــن الوظائــف الجديــدة، وســتظل الوظائــف الإبداعيــة والمعقــدة بحاجــة إلــى العقــل البشــري فــي تنفيذهــا وإدارتهــا"
        )
    },
    {
        "question": "من يتحمل المسؤولية القانونية في حال حدوث أخطاء أو حوادث؟؟",
        "reference": (
            "مــن المهــم تطويــر الأُطــر القانونيــة والتنظيميــة لتتماشــى مــع التطــورات المســتمرة والمتســارعة فــي مجــال الــذكاء الاصطناعــي، ولكــن ســيظل هنــاك تحــدٍ فــي تحديــد المســؤولية، وخاصــة فــي الأعمــال المؤتمتــة بصفــة كاملــة، علــى ســبيل المثــال، مــن ســيكون المســؤول عــن حــوادث الســيارات ذاتيــة القيــادة؟ هــل هــي الشــركة المصنعــة أم مــزود البرمجيــات أو مالــك المركبــة؟"
        ),
    },
    {
        "question": "هل سيتفوق الذكاء الاصطناعي على الذكاء البشري؟",
        "reference": (
            "مــازال الــذكاء الاصطناعــي فــي مراحلــه الأولــى، وأكثــر تطبيقاتــه الموجــودة اليــوم محــدودة المهــام والقــدرات، وبعيــدة جــدًا عــن مســتوى الــذكاء البشــري العــام، ومــن الصعــب حاليًــا تصــور مســتوى الــذكاء الــذي ســتصل إليــه الآلــة فــي المســتقبل")
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

    df = result.to_pandas()  # type: ignore

    print("\n=== PER QUESTION RESULTS ===")
    print(df)

    df.to_csv("evaluation_results.csv", index=False)

    return result


if __name__ == "__main__":
    evaluate_rag()
