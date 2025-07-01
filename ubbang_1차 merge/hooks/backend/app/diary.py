from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List
import os
import openai
from datetime import datetime

from .utils import analyze_emotion, summarize_text, generate_image
from .chat import get_chat_history  # DynamoDB에서 유저 채팅 불러오는 함수
from .diary_db import get_diary_entries
from .diary_db import save_diary_entry


router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")

class DiaryResponse(BaseModel):
    title: str
    content: str
    emotion: str
    summary: str
    image_url: str


class DiaryEntry(BaseModel):
    id: str
    user_id: str
    date: datetime
    title: str
    content: str
    emotion: str
    summary: str
    image_url: str

@router.get("/diary/entries", response_model=List[DiaryEntry])
async def fetch_diary_entries(user_id: str = Query(...)):
    entries = get_diary_entries(user_id)
    return entries

@router.get("/diary", response_model=DiaryResponse)
async def generate_diary(user_id: str = Query(...)):
    chat_history = get_chat_history(user_id)
    combined_text = " ".join([msg["content"] for msg in chat_history if msg["role"] == "user"])

    emotion = analyze_emotion(combined_text)
    summary = summarize_text(combined_text)
    content = f"{summary} 상담을 통해 내 마음을 더 잘 이해하게 되었다."
    title = {
        "happy": "밝은 하루", "sad": "생각이 많은 날", "neutral": "평범한 일상",
        "excited": "설레는 순간", "anxious": "복잡한 하루"
    }.get(emotion, "감정의 기록")
    image_url = generate_image(emotion)

    save_diary_entry(user_id, title, content, emotion, summary, image_url)

    return DiaryResponse(
        title=title,
        content=content,
        emotion=emotion,
        summary=summary,
        image_url=image_url
    )
