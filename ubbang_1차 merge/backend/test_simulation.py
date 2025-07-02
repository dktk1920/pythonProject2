import sys, os, asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

from app.openai_helper import (
    get_chatbot_response, detect_query_type,
    build_system_prompt, get_user_memory
)
from app.retrieval_helper import get_rag_response
from app.naver_helper import get_external_info
from app.chat import save_message

# 테스트용 메시지
test_messages = [
    "나 오늘 진짜 너무 힘들었어",
    "과장님이 또 뭐라고 했어",
    "며칠 전에 내가 왜 울었는지 기억나?",
    "백악기 공룡에 대해서 알려줘",
    "서울 날씨 어때?",
    "나 왜 이렇게 무기력하지?",
    "나 진짜 잘하고 있는 걸까?",
    "안양하이미디어아카데미 어때?",
    "우울해서 아무것도 하기 싫어",
    "회사 퇴사하고 싶어. 어떻게 해야 할까?"
]

# 기본 테스트 유저 정보
user_id = "guest-test-user"
gender = "female"
mode = "banmal"
system_prompt = build_system_prompt(gender, mode)


# ✅ RAG용 더미 메시지 저장 함수
def preload_test_messages():
    print("📝 테스트용 메시지를 DynamoDB에 저장 중...")

    sample_conversations = [
        ("user", "며칠 전에 진짜 속상한 일 있었어"),
        ("assistant", "무슨 일 있었는지 말해줘. 내가 들어줄게."),
        ("user", "친한 친구한테 실망했어"),
        ("assistant", "아 진짜? 어떤 상황이었는데?"),
        ("user", "내가 힘들 때 도와주지도 않고 오히려 날 무시했어"),
        ("assistant", "헐, 그건 좀 너무하네. 너 진짜 많이 속상했겠다.")
    ]

    for role, content in sample_conversations:
        save_message(user_id, role, content)


# ✅ 테스트 실행 함수
async def run_test():
    memory = get_user_memory(user_id)

    for i, msg in enumerate(test_messages):
        print(f"\n📨 [{i+1}] 유저 입력: {msg}")
        query_type = detect_query_type(msg)
        print(f"🔍 쿼리 유형: {query_type}")

        if query_type == "일반대화":
            reply = await get_chatbot_response(user_id, msg, system_prompt)
        elif query_type == "개인기록검색":
            reply = await asyncio.to_thread(get_rag_response, msg, user_id, system_prompt, memory)
        elif query_type == "외부정보검색":
            reply = await asyncio.to_thread(get_external_info, msg, system_prompt, memory)
        else:
            reply = "🤖 해당 쿼리 유형에 대한 처리가 아직 구현되지 않았습니다."

        print(f"🤖 챗봇 응답: {reply}")


# ✅ 메인 실행
if __name__ == "__main__":
    preload_test_messages()           # 💾 더미 데이터 먼저 저장
    asyncio.run(run_test())           # 🧪 테스트 실행
