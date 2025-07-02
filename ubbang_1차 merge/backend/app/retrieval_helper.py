# 외부정보 RAG
# pip install langchain langchain-community langchain-openai chromadb 설치해야댐



# 내부정보(대화기반) RAG
# ✅ retrieval_helper.py
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI

import boto3
from boto3.dynamodb.conditions import Key
import os
from dotenv import load_dotenv

load_dotenv()


# ✅임베딩 설정
embedding = OpenAIEmbeddings(model="text-embedding-3-small")


# ✅ 유저 대화 불러오기
def load_user_documents(user_id: str) -> list[Document]:
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
    table = dynamodb.Table(os.getenv("DYNAMO_TABLE_NAME", "ChatMessages"))

    response = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id),
        ScanIndexForward=True,
        Limit=100
    )

    items = response.get("Items", [])
    docs = []
    for item in items:
        content = item.get("content", "")
        role = item.get("role", "")
        if role in ("user", "assistant"):
            docs.append(Document(page_content=content, metadata={"user_id": user_id}))
    return docs

# ✅ 벡터스토어 생성
def create_vectorstore_from_user_logs(user_id: str) -> FAISS:
    documents = load_user_documents(user_id)
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)
    return FAISS.from_documents(split_docs, embedding=embedding)

# ✅ RAG 응답 생성
def get_rag_response(message: str, user_id: str, system_prompt: str, memory) -> str:
    vectorstore = create_vectorstore_from_user_logs(user_id)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    docs = retriever.get_relevant_documents(message)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("user", "다음은 너랑 유저가 예전에 했던 대화들이야. 말투는 시스템 프롬프트 모드 설정값으로 유지해. 이걸 참고해서 지금 유저가 한 질문에 자연스럽게 대답해줘.\n\n{context}\n\n질문: {question}")
    ])

    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    chain = create_stuff_documents_chain(llm, prompt)

    return chain.invoke({
        "system_prompt": system_prompt,
        "question": message,
        "context": docs
    })
