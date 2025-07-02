import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 로드
load_dotenv()
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트
client = OpenAI(api_key=OPENAI_API_KEY)

# 네이버 API 헤더 설정
headers = {
    "X-Naver-Client-Id": NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
}


def fetch_naver_results(query: str, category: str):
    """
    네이버 블로그, 뉴스, 지식iN 중 하나를 category로 받아 검색 결과 가져옴
    """
    url = f"https://openapi.naver.com/v1/search/{category}.json"
    params = {"query": query, "display": 5}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        res.raise_for_status()
        return res.json().get("items", [])
    except Exception as e:
        print(f"[ERROR] {category} 검색 실패: {e}")
        return []


def format_results(items: list, label: str) -> str:
    """
    검색 결과를 사람이 보기 쉽게 포맷팅
    """
    if not items:
        return f"{label} 없음\n"

    result = f"📌 [{label}]\n"
    for item in items:
        title = item.get("title", "").replace("<b>", "").replace("</b>", "")
        desc = item.get("description", "").replace("<b>", "").replace("</b>", "")
        result += f"{title} — {desc}\n"
    return result.strip()


def get_external_info(query: str, system_prompt: str, memory) -> str:
    """
    외부 정보 검색 통합 함수: 블로그 + 뉴스 + 지식iN
    결과 요약은 OpenAI로 처리
    """
    # 네이버 검색
    blog_items = fetch_naver_results(query, "blog")
    news_items = fetch_naver_results(query, "news")
    kin_items = fetch_naver_results(query, "kin")

    # 포맷팅
    combined_text = (
        format_results(news_items, "뉴스") + "\n\n" +
        format_results(blog_items, "블로그") + "\n\n" +
        format_results(kin_items, "지식iN")
    )

    # 요약 프롬프트
    prompt = f"""

사용자 질문: "{query}"

검색 결과:
{combined_text}

아래는 네이버 뉴스/블로그/지식iN에서 찾은 검색 결과야.
이 내용을 참고해서 최대한 정확하게, 친구처럼 대답해줘.
말투는 system_prompt로 설정된 반말/존댓말을 그대로 유지해야 해.

요약만 하지 말고, 실제 내용을 인용해서 설명하고,
사람이 말하듯 자연스럽게 이어줘.


""".strip()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] 외부 정보 요약 실패: {e}"
