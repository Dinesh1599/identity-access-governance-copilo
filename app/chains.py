from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from .rag_index import build_or_load_index



llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)


# 1) Anomaly Summary
summary_prompt = ChatPromptTemplate.from_messages([
("system", "You are a security analyst. Summarize the anomaly in 120 words max."),
("human", "Anomaly JSON: {anomaly}\nReturn: concise summary and likely risk."),
])


def summarize_anomaly(anomaly: Dict[str, Any]) -> str:
    msg = summary_prompt.format_messages(anomaly=anomaly)
    return llm.invoke(msg).content


# 2) Least-Privilege Decision helper
decision_prompt = ChatPromptTemplate.from_messages([
("system", "You recommend least-privilege changes for IAM access."),
("human", "User: {user}\nCurrent: {current}\nRequested: {requested}\nReturn: grant/deny rationale and safer alternative.")
])


def least_privilege_decision(user: Dict[str, Any], current: list[str], requested: list[str]) -> str:
    current_str = ", ".join(current)
    requested_str = ", ".join(requested)
    msg = decision_prompt.format_messages(
        user=user,
        current=current_str,
        requested=requested_str,
    )
    return llm.invoke(msg).content



# 3) Policy Q&A via RAG
qa_prompt = ChatPromptTemplate.from_messages([
("system", "Answer using the provided policy context. If not in context, say so."),
("human", "Question: {question}\nContext: {context}")
])


def policy_qa(question: str) -> str:
    store = build_or_load_index()
    docs = store.similarity_search(question, k=4)
    context = "\n---\n".join([d.page_content[:1200] for d in docs])
    msg = qa_prompt.format_messages(question=question, context=context)
    return llm.invoke(msg).content