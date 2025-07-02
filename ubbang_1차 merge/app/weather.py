# app/weather.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city="서울"):
    # ✅ 한글 → 영어 도시 매핑
    city_map_ko_en = {
        "서울": "Seoul",
        "부산": "Pusan",
        "인천": "Incheon",
        "대구": "Daegu",
        "대전": "Daejeon",
        "광주": "Gwangju",
        "수원": "Suwon",
        "울산": "Ulsan",
        "전주": "Jeonju",
        "청주": "Cheongju"
    }

    # 매핑된 영어 도시명으로 변환 (없으면 그대로 사용)
    city_query = city_map_ko_en.get(city, city)

    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city_query}&lang=ko"
    response = requests.get(url)
    data = response.json()

    # ❗에러 응답 방지
    if "location" not in data:
        return f"❌ '{city}'에 대한 날씨 정보를 찾을 수 없어요."

    # ✅ 영어 → 한글 도시명 매핑
    city_name_map = {v: k for k, v in city_map_ko_en.items()}

    english_name = data["location"]["name"]
    korean_name = city_name_map.get(english_name, english_name)
    condition_text = data["current"]["condition"]["text"]
    temperature = data["current"]["temp_c"]

    # ✅ 날씨 이모지
    weather_icon_map = {
        "맑음": "☀️",
        "대체로 맑음": "🌤️",
        "부분적으로 흐림": "⛅",
        "흐림": "☁️",
        "안개": "🌫️",
        "비": "🌧️",
        "소나기": "🌦️",
        "천둥번개": "⛈️",
        "진눈깨비": "🌨️",
        "눈": "❄️",
    }
    icon = weather_icon_map.get(condition_text, "")
    description = f"{icon} {condition_text}" if icon else condition_text

    # ✅ 이상치 필터링
    if not (-30 <= temperature <= 40):
        return f"{korean_name}의 현재 날씨는 {description}입니다. 다만 기온 정보는 신뢰하기 어려워요."

    return f"{korean_name}의 현재 날씨는 {description}이고, 기온은 {temperature}°C입니다."

