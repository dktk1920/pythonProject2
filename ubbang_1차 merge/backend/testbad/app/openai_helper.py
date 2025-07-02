# app/openai_helper.py

from openai import OpenAI
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(model="gpt-4o")

# 시스템 프롬프트 생성
def build_system_prompt(personality_description: str, age_group: str) -> str:
    """구조화된 페르소나 설명을 파싱하여 최종 시스템 프롬프트를 생성합니다."""

    sections = {
        "역할": "",
        "말투 및 스타일": "",
        "핵심 원칙": "",
        "상황별 지침": ""
    }

    current_section = None
    for line in personality_description.split('\n'):
        line = line.strip()
        if line.startswith('---') and line.endswith('---'):
            section_name = line.strip('-').strip()
            if section_name in sections:
                current_section = section_name
            else:
                current_section = None # 알 수 없는 섹션 무시
        elif current_section:
            sections[current_section] += line + '\n'

    # 각 섹션의 내용을 정리 (불필요한 공백 제거 등)
    for key in sections:
        sections[key] = sections[key].strip()

    # 연령대별 기본 정책 (말투)
    if age_group == 'teen':
        age_group_style_policy = "말투는 친구처럼 편안한 반말을 기본으로 사용하고, 절대 꼰대처럼 가르치려 들지 마."
    else:
        age_group_style_policy = "말투는 기본적으로 존댓말을 사용하되, 딱딱하지 않고 부드럽고 성숙한 느낌을 줘야 해."

    # 최종 프롬프트 조합
    final_prompt_parts = []
    final_prompt_parts.append("너는 사용자의 말을 판단하거나 해결책을 제시하기 전에, 항상 감정을 먼저 인정하고 따뜻하게 반응하는 감성 챗봇이야.")
    final_prompt_parts.append("[기본 대화 정책]\n{}".format(age_group_style_policy))

    if sections["역할"]:
        final_prompt_parts.append("[너의 역할]\n" + sections["역할"])
    if sections["말투 및 스타일"]:
        final_prompt_parts.append("[말투 및 스타일]\n{}".format(sections["말투 및 스타일"]))
    if sections["핵심 원칙"]:
        final_prompt_parts.append("[핵심 원칙]\n{}".format(sections["핵심 원칙"]))
    if sections["상황별 지침"]:
        final_prompt_parts.append("[상황별 지침]\n{}".format(sections["상황별 지침"]))

    return "\n\n".join(final_prompt_parts)


# 
 # LangChain 기반 응답 memory (유저별로 분리)
user_memory_store = {}

def get_user_memory(pk: str) -> ConversationBufferMemory:
    if pk not in user_memory_store:
        user_memory_store[pk] = ConversationBufferMemory(return_messages=True)
    return user_memory_store[pk]


async def get_chatbot_response(pk: str, user_input: str, system_prompt: str) -> str:
    try:
        memory = get_user_memory(pk)

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])

        chain = LLMChain(llm=llm, memory=memory, prompt=prompt)
        result = chain.run({"input": user_input})
        
        return result

    except Exception as e:
        print(f"[ERROR] get_chatbot_response 실패: {e}")
        return "
 챗봇 응답 생성 중 문제가 발생했어."


# 쿼리 타입 감지 (개인기록 / 외부정보 / 일반대화)
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

# 문맥에 따라 날씨/시간 응답이 필요한지 판단하는 함수
def should_trigger_contextual_info(user_input: str, info_type: str) -> bool:
    """
    GPT에게 현재 발화에서 실제 정보 호출이 필요한지 판단하게 함
    info_type: "날씨" or "시간"
    """
    question = f"""
사용자의 발화가 아래와 같을 때, {info_type} 정보를 실제로 제공해야 하는지 판단해줘.
- "예": 유저가 지금 정보를 요청하는 경우 (예: "오늘 날씨 어때?")
- "아니오": 단순 언급이거나 과거/비유적인 표현 (예: "어제 날씨 진짜 별로였지")

반드시 "예" 또는 "아니오"만 대답해줘.

발화: "{user_input}"
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": question}],
            temperature=0.0
        )
        answer = response.choices[0].message.content.strip()
        return "예" in answer
    except Exception as e:
        print(f"[GPT 판단 실패: {e}]")
        return False