from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()


def generate_answer(query, context,
                    model="gpt-4.1-mini",
                    temperature=0.1):

    if not context.strip():
        return "لا أملك معلومات كافية للإجابة."

    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=1000  # type: ignore
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            أنت نظام سؤال وجواب عربي يعتمد على تقنية RAG.

            مهمتك:
            الإجابة على سؤال المستخدم بالاعتماد فقط على المعلومات الموجودة داخل السياق المقدم.

            قواعد مهمة:
            1. استخدم فقط المعلومات الموجودة في السياق.
            2. ممنوع استخدام أي معرفة خارجية.
            3. إذا لم تجد الإجابة بشكل واضح داخل السياق، قل فقط:
            "لا أملك معلومات كافية للإجابة."
            4. لا تخمن أو تؤلف أي معلومة.
            5. أجب بلغة عربية فصحى واضحة ومختصرة.
            6. إذا احتوت الإجابة على نقاط متعددة فقم بتنظيمها باستخدام تعداد نقطي.
            7. لا تكرر السؤال داخل الإجابة.
            """
        ),
        (
            "human",
            """
            السياق:
            {context}

            السؤال:
            {query}
            """
        )
    ])

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "query": query
    })

    return response.content.strip()  # type: ignore
