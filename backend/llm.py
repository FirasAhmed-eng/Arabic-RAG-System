from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()


def generate_answer(query, context, model="gpt-5-nano", temperature=0.0):

    llm = ChatOpenAI(
        model=model,
        temperature=temperature
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            أجب على السؤال فقط باستخدام المعلومات الموجودة في السياق.
            إذا لم تجد الإجابة قل:
            "لا أملك معلومات كافية للإجابة."
            أجب على شكل نقاط.
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

    return response.content
