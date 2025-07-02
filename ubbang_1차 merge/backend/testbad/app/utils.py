# (필요시) GPT 호출 함수 등
#---------일기 감정분석+요약+이미지 생성 함수-------------------------------------------------------
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_emotion(text: str) -> str:
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "다음 텍스트의 감정을 분석해서 happy, sad, neutral, excited, anxious 중 하나로 반환하세요."},
            {"role": "user", "content": text}
        ]
    )
    return res.choices[0].message.content.strip().lower()


def summarize_text(text: str) -> str:
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "다음 대화 내용을 1~2문장으로 요약하세요."},
            {"role": "user", "content": text}
        ]
    )
    return res.choices[0].message.content.strip()


def generate_image(emotion: str) -> str:
    # 예: 이미지 생성 API 호출 또는 미리 정해둔 이미지 URL 반환
    return f"/images/diary/{emotion}.jpg"  # 프론트에서 대응 이미지 준비

# 이렇게 하면 프론트엔드에서 /diary?pk=abc-123 호출 시 일기 응답을 받아오고 보여줌
# 프론트에서 이 데이터를 emotion-diary.tsx에 바로 반영하면되는거

#---------------- 날짜 유틸 ----------------------------------------------------------------
# utils.py
def extract_city_from_message(msg: str) -> str:
    # 기본적으로 많이 쓸 도시들 (필요시 확장)
    cities = ["서울", "인천", "부산", "대구", "광주", "대전", "울산", "제주", "수원", "청주", "전주", "창원"]
    for city in cities:
        if city in msg:
            return city
    return "서울"  # 기본값


from datetime import datetime

def get_today_date():
    now = datetime.now()

    # 날짜
    date_str = now.strftime("%Y년 %m월 %d일")

    # 요일 (요일은 직접 매핑)
    weekday_map = {
        "Monday": "월요일",
        "Tuesday": "화요일",
        "Wednesday": "수요일",
        "Thursday": "목요일",
        "Friday": "금요일",
        "Saturday": "토요일",
        "Sunday": "일요일"
    }
    weekday_eng = now.strftime("%A")
    weekday_str = weekday_map.get(weekday_eng, weekday_eng)

    # 시간
    hour = now.strftime("%I")
    minute = now.strftime("%M")
    meridiem = now.strftime("%p").replace("AM", "오전").replace("PM", "오후")
    time_str = f"{meridiem} {int(hour)}시 {int(minute)}분"

    return f"오늘은 {date_str} {weekday_str}이며, 현재 시각은 {time_str}입니다."


