# redis_chat_save.py
# 캐시: 자주 사용되는 데이터를 임시로 저장해두는 저장소, DB나 서버 대신 사용하는 임시 저장 공간
# 메모리 기반 저장소라 DB보다 수십배 빠름, 같은 데이터를 반복 조회할 떄 서버 부하를 줄임
from redis import Redis
import json

#port=6379: 기본 Redis 포트 , decode_responses=True: Redis 응답을 문자열로 반환하도록 설정(바이트X)
redis = Redis(host="localhost", port=6379, decode_responses=True)

########채팅 메시지 저장 기능########

#채팅 메시지 저장(최근 10개의 메시지만 유지)
def save_chat_message(user_id: str, timestamp: str, message: str, emotion: str, keywords: list):
    key = f"chat:{user_id}"
    data = {
        "userId": user_id,
        "timestamp": timestamp,
        "message": message
    }
    redis.rpush(key, json.dumps(data))
    redis.ltrim(key, -10, -1)

#최근 채팅 메시지 불러오기
def get_recent_messages(user_id: str):
    raw = redis.lrange(f"chat:{user_id}", 0, -1)
    return [json.loads(entry) for entry in raw]

#사용자 정보 캐시에 저장(Redis는 문자열만 저장 가능하기에 json.dumps()로 문자열로 변환)
def cache_user_info(user_id: str, user_data: dict):
    redis.set(f"user:{user_id}", json.dumps(user_data))

#사용자 정보 캐시에서 가져오기()
def get_cached_user_info(user_id: str):
    data = redis.get(f"user:{user_id}")
    return json.loads(data) if data else None

