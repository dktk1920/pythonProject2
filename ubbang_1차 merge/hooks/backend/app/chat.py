from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from openai import OpenAI
import os
from dotenv import load_dotenv

from .openai_helper import build_system_prompt, get_chatbot_response
from .weather import get_weather
from .utils import extract_city_from_message, get_today_date

import boto3
from boto3.dynamodb.conditions import Key
import uuid, time

# ───────────────────────────────────────────────────────
load_dotenv()
router = APIRouter()
connections = {}

# ✅ DynamoDB 설정
dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
table = dynamodb.Table(os.getenv("DYNAMO_TABLE_NAME", "ChatMessages"))

# ───────────────────────────────────────────────────────

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    pk = websocket.query_params.get("pk")  # ✅ pk는 파티션 키
    user_id = websocket.query_params.get("userId")  # 참고용
    gender = websocket.query_params.get("gender", "female")
    mode = websocket.query_params.get("mode", "banmal")

    if not pk:
        await websocket.close()
        return

    await websocket.accept()

    # 시스템 프롬프트 세팅
    system_prompt = build_system_prompt(gender, mode)
    history = [{"role": "system", "content": system_prompt}]
    connections[websocket] = history

    try:
        while True:
            msg = await websocket.receive_text()
            history.append({"role": "user", "content": msg})

            # ✅ 유저 메시지 → DynamoDB 저장
            save_message_to_dynamo(pk, user_id, "user", msg, gender)

            # 날짜/날씨 응답
            response_parts = []
            if "날씨" in msg:
                city = extract_city_from_message(msg)
                response_parts.append(get_weather(city))

            if any(word in msg for word in ["날짜", "오늘", "지금", "몇시"]):
                response_parts.append(get_today_date())

            if response_parts:
                reply = " ".join(response_parts)
            else:
                try:
                    print("📤 GPT 요청 history:", history)
                    reply = await get_chatbot_response(history)
                    print(f"🎯 GPT 응답 수신 완료: {reply[:30]}")
                    await websocket.send_text(reply)
                    print("📥 GPT 응답:", repr(reply))
                except Exception as gpt_error:
                    print("❌ GPT 호출 실패:", gpt_error)
                    reply = "AI 응답 생성 중 오류가 발생했어요."

            # 방어: 응답이 None이거나 비어있을 경우 처리
            if not reply:
                reply = "음... 무슨 말을 해줘야 할지 모르겠어 😅"

            history.append({"role": "assistant", "content": reply})

            # ✅ GPT 응답 → DynamoDB 저장
            save_message_to_dynamo(pk, user_id, "assistant", reply, gender)

            try:
                safe_reply = reply.encode("utf-8", "replace").decode("utf-8")
                await websocket.send_text(safe_reply)
            except Exception as e:
                print("[ERROR] WebSocket 응답 실패:", e)
                await websocket.send_text("⚠️ 응답 중 오류가 발생했어요. 다시 시도해 주세요.")

    except WebSocketDisconnect:
        connections.pop(websocket, None)

# ───────────────────────────────────────────────────────
# ✅ DynamoDB 저장 함수
def save_message_to_dynamo(pk: str, user_id: str, role: str, content: str, gender: str):
    try:
        message_item = {
            "pk": str(pk),                         # 파티션 키
            "timestamp": int(time.time()),         # 정렬 키
            "user_id": str(user_id),               # 참고용
            "gender": gender,                      # ✅ 성별 저장
            "role": role,                          # user or assistant
            "content": content,
            "message_id": str(uuid.uuid4())        # 고유 메시지 ID
        }
        table.put_item(Item=message_item)
    except Exception as e:
        print(f"[ERROR] 메시지 저장 실패: {e}")

# ───────────────────────────────────────────────────────
# ✅ 채팅 기록 조회 함수
def get_chat_history(pk: str, limit: int = 50) -> list[dict]:
    try:
        response = table.query(
            KeyConditionExpression=Key("pk").eq(pk),
            ScanIndexForward=False,
            Limit=limit,
        )
        items = response.get("Items", [])
        return sorted(items, key=lambda x: x.get("timestamp", 0))
    except Exception as e:
        print(f"[ERROR] 채팅 기록 조회 실패: {e}")
        return []
