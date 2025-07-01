from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

from .openai_helper import build_system_prompt, get_chatbot_response

import boto3
from boto3.dynamodb.conditions import Key


from .weather import get_weather
from .utils import extract_city_from_message
from .utils import get_today_date


# --------------------------------------------------------------------------------

load_dotenv()
router = APIRouter()

connections = {}


# DynamoDB 설정
dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
table = dynamodb.Table(os.getenv("DYNAMO_TABLE_NAME", "ChatMessages"))

#-----------------------------------------------------------------------------------

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    gender = websocket.query_params.get("gender", "female")   # 기본값 : 여성유저
    mode = websocket.query_params.get("mode", "banmal")       # 기본값 : 반말

    await websocket.accept()

    # 시스템 프롬프트 적용
    system_prompt = build_system_prompt(gender, mode)
    history = [{"role": "system", "content": system_prompt}]
    connections[websocket] = history

    try:
        while True:
            msg = await websocket.receive_text()
            history.append({"role": "user", "content": msg})

            # ✅ 유저 메시지에 날짜/날씨 키워드가 포함된 경우 → GPT 호출 전에 응답
            response_parts = []

            if "날씨" in msg:
                city = extract_city_from_message(msg)
                response_parts.append(get_weather(city))

            if "날짜" in msg or "오늘" in msg or "지금" in msg or "몇시" in msg:
                response_parts.append(get_today_date())

            if response_parts:
                reply = " ".join(response_parts)
            else:
                # 그 외는 GPT 응답 생성
                reply = await get_chatbot_response(history)


            history.append({"role": "assistant", "content": reply})

            # ✅ WebSocket 전송 시 유니코드 깨짐 방지 처리
            try:
                safe_reply = reply.encode("utf-8", "replace").decode("utf-8")
                await websocket.send_text(safe_reply)
            except Exception as e:
                print("[ERROR] WebSocket 응답 실패:", e)
                await websocket.send_text("⚠️ 응답 중 오류가 발생했어요. 다시 시도해 주세요.")

    except WebSocketDisconnect:
        connections.pop(websocket, None)


# ------- 채팅 내역 저장 함수 ----------------------
def get_chat_history(user_id: str, limit: int = 50) -> list[dict]:
    """
    해당 user_id의 최근 채팅 기록을 DynamoDB에서 가져온다.
    기본적으로 최근 50개까지 가져옴.
    """
    try:
        response = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
            ScanIndexForward=False,  # 최신 순으로 정렬
            Limit=limit,
        )
        items = response.get("Items", [])
        # 시간순 정렬 (오래된 → 최신)
        return sorted(items, key=lambda x: x.get("timestamp", 0))

    except Exception as e:
        print(f"[ERROR] 채팅 기록 조회 실패: {e}")
        return []

# 다이나모 밑의 예시를 기준으로 작성된거임
# user_id를 파티션 키로 사용할 떄 기준!!
# {
#   "user_id": "abc-123",
#   "message_id": "uuid-456",
#   "role": "user",         // 또는 "assistant"
#   "content": "오늘 너무 피곤했어요.",
#   "timestamp": 1710000000
# }
