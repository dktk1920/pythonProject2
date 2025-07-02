
# 6/30 업데이트 -----------------------------------------------
# history 리스트 제거, 대신 get_chatbot_response(user_id, message) 호출
# query_params에서 user_id도 함께 받도록 수정

# 7/1 업데이트 -------------------------------------------------
# 반말/존댓말 모드 + RAG/GPT 분기 + 외부검색 통합
# 비회원 유저만 DynamoDB에 유저/챗봇 쌍으로 저장 + 성별 포함

# ✅ chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import os, uuid, time, asyncio
from dotenv import load_dotenv
import boto3
from boto3.dynamodb.conditions import Key

from .openai_helper import (
    build_system_prompt, get_chatbot_response,
    get_user_memory, detect_query_type,should_trigger_contextual_info
)
from .weather import get_weather
from .utils import extract_city_from_message, get_today_date
from .retrieval_helper import get_rag_response
from .naver_helper import get_external_info


load_dotenv()
router = APIRouter()
dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
table = dynamodb.Table(os.getenv("DYNAMO_TABLE_NAME", "ChatMessages"))


def save_message(user_id: str, role: str, content: str):
    try:
        if user_id.startswith("guest"):
            table.put_item(
                Item={
                    "user_id": user_id,
                    "message_id": str(uuid.uuid4()),
                    "role": role,
                    "content": content,
                    "timestamp": int(time.time())
                }
            )
    except Exception as e:
        print(f"[ERROR] 메시지 저장 실패: {e}")


def get_chat_history(user_id: str, limit: int = 50) -> list[dict]:
    try:
        response = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
            ScanIndexForward=False,
            Limit=limit,
        )
        items = response.get("Items", [])
        return sorted(items, key=lambda x: x.get("timestamp", 0))
    except Exception as e:
        print(f"[ERROR] 채팅 기록 조회 실패: {e}")
        return []


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    gender = websocket.query_params.get("gender", "female")
    mode = websocket.query_params.get("mode", "banmal")
    user_id = websocket.query_params.get("user_id", f"guest-{str(uuid.uuid4())}")

    await websocket.accept()

    memory = get_user_memory(user_id)
    system_prompt = build_system_prompt(gender, mode)
    memory.chat_memory.messages = []


    try:
        while True:
            msg = await websocket.receive_text()
            save_message(user_id, "user", msg)

            response_parts = []
            if "날씨" in msg and should_trigger_contextual_info(msg, "날씨"):
                city = extract_city_from_message(msg)
                response_parts.append(get_weather(city))

            if "몇시" in msg and should_trigger_contextual_info(msg, "시간"):
                response_parts.append(get_today_date())

            if response_parts:
                reply = " ".join(response_parts)
            else:
                query_type = await asyncio.to_thread(detect_query_type, msg)

                if query_type == "개인기록검색":
                    reply = await asyncio.to_thread(get_rag_response, msg, user_id, system_prompt, memory)
                elif query_type == "외부정보검색":
                    reply = await asyncio.to_thread(get_external_info, msg, system_prompt, memory)

                else:
                    reply = await get_chatbot_response(user_id, msg, system_prompt)

            save_message(user_id, "assistant", reply)
            memory.chat_memory.add_user_message(msg)
            memory.chat_memory.add_ai_message(reply)

            try:
                await websocket.send_text(reply)
            except Exception:
                await websocket.send_text("⚠️ 응답 전송 중 오류 발생!")

    except WebSocketDisconnect:
        pass
