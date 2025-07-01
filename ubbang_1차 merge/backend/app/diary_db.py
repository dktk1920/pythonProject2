import boto3
from boto3.dynamodb.conditions import Key
import uuid
from datetime import datetime


dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
diary_table = dynamodb.Table("DiaryEntries")  # 테이블 이름 정확히 확인

def get_diary_entries(user_id: str) -> list[dict]:
    try:
        response = diary_table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
            ScanIndexForward=False
        )
        return response.get("Items", [])
    except Exception as e:
        print(f"[ERROR] Diary 조회 실패: {e}")
        return []


# 생성된 일기 저장
def save_diary_entry(user_id: str, title: str, content: str, emotion: str, summary: str, image_url: str):
    item = {
        "user_id": user_id,
        "id": str(uuid.uuid4()),
        "date": datetime.utcnow().isoformat(),
        "title": title,
        "content": content,
        "emotion": emotion,
        "summary": summary,
        "image_url": image_url,
    }

    diary_table.put_item(Item=item)
    return item  # 저장한 데이터 반환
