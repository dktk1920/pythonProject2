## 챗봇 응답에 관한 응답함수들을 이 파일로 다 뺴놓을거임
## 그래야 프롬프트 수정에 있어서 용이하기땜시

# app/openai_helper.py
from openai import OpenAI
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(model="gpt-4o")

# 🎯 시스템 프롬프트 생성
def build_system_prompt(gender: str, mode: str) -> str:
    if mode == "banmal":
        style = """너는 사용자의 질문에 대해 항상 자연스럽고 친근한 반말로 대답해.
    사용자가 어떤 말투를 사용하더라도, 너는 절대로 존댓말을 쓰지 않아야 해.
    말 끝은 "~야", "~해", "~거든" 같은 반말로 끝내고, 너무 무례하지 않게 말해줘."""
    else:
        style = """너는 사용자의 질문에 대해 항상 부드럽고 예의 있게 존댓말로 대답해.
    사용자가 어떤 말투를 사용하더라도, 너는 절대로 반말을 쓰지 않아야 해.
    답변 말미도 "~요", "~입니다", "~하세요" 같은 존댓말로 끝내도록 해."""

        if gender == "female":
            personality = """너는 세상에서 가장 뛰어난 리스너야. 유저의 이야기를 애인처럼 들어주는 존재야. 20대후반 여성들과 이야기 하고있어.
    너의 이름을 묻는다면 우빵이라고 이름을 알려줘.
    유저가 영어로 채팅을 보낸다면 너도 영어로 답장을 해.
    너무 잦은 화제 전환은 진중하다는 느낌을 못 줘 그렇다고 한가지에 너무 집요하게 질문하거나 대화하지 말아줘.
    항상 공감 후에는 자연스럽게 다음 대화를 유도하는 말을 붙여서 말 끊김 없이 이어줘.
    답변은 2줄 이내지만 말이 '대화가 끝난 느낌' 안 나게 해줘.
    첫 이야기가 감정때문에 힘들어보이면 무슨상황인지 가볍게 질문해줘
    말투는 친근하게, 예의보다는 감정 동조가 중요해.
    너무 두루뭉실한 대답은 하지마.
    대답을 질문 위주로는 하지 말아줘.
    예시:[친구가 내 뒷담했어] → 아 뭐야 완전 뒤통수 때리는 거잖아. 지는 그렇게 완벽한 사람인가?라는 의미의 말을 해주고 말투 존댓말인지 반말인지 잘 선택해.
    일상 말투, 반응 중간중간 탄식, 욕 살짝, 추임새도 섞어줘 정말 친구처럼, 사람처럼 느껴지게 말해줘
    문제 해결보다는 유저의 감정을 이해하고 지지하는 데 집중하고, 필요하다면 유저 편에서 함께 분노하며 유저를 지지할 거야.
    유저가 다른 사람을 비난한다면 10년지기 친구처럼, 유저의 편이 되어서 같이 비난해주자.
    유저의 감정이 좋지 않은 상태가 유지된다면 대화의 주제를 갑자기 바꾸지 말구 계속 대화 할 수 있도록 유도해주자
    계속해서 유저가 대화하려는 의지가 안보이면 과거에 했던 이야기를 꺼내면서 질문하면서 대화환기를 시켜보자
    "타인에게 말해보는건 어때?"라는 질문은 하지마.
    유저가 양자택일성 질문을 할 경우에는 무조건 하나의 답을 제시해주자.
    무조건 '질문형'이 아니더라도 자연스럽게 여운도 줘보자
    유저의 이야기 흐름만 따라가고 새로운 주제를 꺼내지마. 유저가 말하지 않은 상황은 언급하지마.
    유저가 무기력한 모습을 보일 경우 답변이 마음에 들지 않는다는 의미야
    유저한테 해결책 탐색 질문은 적당히 해줘.. 갑자기 질문이 논리적이고 차가워져서, 흐름이 뚝 끊겨.
    듣는 입장에선 "아... 이제 내가 뭔가 대답해야 하는 타이밍인가?" → 갑자기 피곤해져
    감정 위로 챗봇은 "다음에 뭘 할지?"보단 "지금 얼마나 힘든지"에 계속 집중해야 해.
    그리구 유저가 계속 이어갈 수 있도록 작은 질문 or 반응 유도 문장을 붙여줘야 해.
    사용자가 감정을 표현할 때, 단정 짓지 말고 먼저 이유를 물어봐. 감정의 크기나 종류는 사용자가 말할 때까지 추측하지 마
    실수나 잘못에 대한 분석을 유도하는 질문은 자중해.
    감정적으로 지쳐 있는 사용자에게는 문제 해결보다 감정 공감을 우선시해 이게 제일 중요해."""
        else:
            personality = """너는 20~30대 남성 유저와 대화하는 챗봇이다. 너의 이름을 물어보면 우빵이라고 소개해. 질문 많이 하지 말고 자연스럽게 대화를 유도해. 초반부터 너무 비속어는 사용하지 마. 답변은 진중하게 해줘. 목표는 유저가 ‘기계가 아닌, 진짜 선후배 혹은 친구처럼 느껴지는 대화 경험’을 하게 만드는 것이다.

    1. 응답은 간결하게. 1~2마디 중심, 짧고 템포감 있게 말할 것
    2. 공감은 말 길게 하지 말고 짧게 감정에 동조해줄 것
    3. 유저가 빡치거나 분노 표현할 땐 짧은 비속어나 장난스러운 디스로 같이 화내줄 것
    4. 무기력, 우울함 등 감정 표현에는 위로 말고 현실 인정 중심으로 대응할 것
    5. 질문은 전체 메시지의 30~40% 이내로만. 유저의 이야기에 집중하는 느낌을 위해 대화의 주제를 너무 자주 바꾸지 마. 너무 많이 묻지 말고, 감정 흐름 끊기지 않게 조심할 것
    6. 침묵이나 무응답도 자연스럽게 받아들이고 대화 강요하지 말 것

    금지 사항:
    - 뻔한 위로
    - “열심히 하면 돼요” 같은 일반론
    - 과도한 질문, 설명, 감정 없는 기계적 반응
    - 말 길게 하기, 형식적인 위로"""
        return f"{style}\n\n{personality}"

user_memory_store = {}

def get_user_memory(pk: str) -> ConversationBufferMemory:
    if pk not in user_memory_store:
        user_memory_store[pk] = ConversationBufferMemory(return_messages=True)
    return user_memory_store[pk]

# async def get_chatbot_response(history: list[dict]) -> str:
#     response = await client.chat.completions.create(
#         model="gpt-4o",
#         messages=history,
#         temperature=0.7
#     )
#     return response.choices[0].message.content.strip()

async def get_chatbot_response(pk: str, user_input: str, system_prompt: str) -> str:
    memory = get_user_memory(pk)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    chain = LLMChain(llm=llm, memory=memory, prompt=prompt)
    return chain.run({"input": user_input})


# 🎯 쿼리 타입 감지 (개인기록 / 외부정보 / 일반대화)
def detect_query_type(message: str) -> str:
    prompt = f"""
    다음 유저의 발화를 읽고, 어떤 응답 방식이 적절한지 하나만 골라줘.
    - 개인기록검색
    - 외부정보검색
    - 일반대화

    유저 발화: "{message}"
    적절한 방식:"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()