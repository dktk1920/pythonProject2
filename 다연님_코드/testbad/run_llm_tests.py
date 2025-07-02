

import asyncio
import json
import os
import sys
from dotenv import load_dotenv

# --- 수정된 부분 ---
# .env 파일이 backend 폴더 안에 있으므로, 정확한 경로를 지정하여 로드합니다.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dotenv_path = os.path.join(project_root, 'backend', '.env')

# .env 파일이 존재하는지 확인하고 로드합니다.
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"[ERROR] .env 파일을 찾을 수 없습니다: {dotenv_path}")
    print("테스트를 진행하려면 backend 폴더에 .env 파일을 생성하고 OPENAI_API_KEY를 설정해야 합니다.")
    sys.exit(1)

# 프로젝트 루트를 sys.path에 추가하여 backend 모듈을 임포트할 수 있도록 함
sys.path.insert(0, project_root)
# --- 수정 완료 ---

from backend.app.openai_helper import get_chatbot_response, build_system_prompt

def load_scenarios(file_path):
    """JSON 파일에서 테스트 시나리오를 로드합니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("scenarios", [])
    except FileNotFoundError:
        print(f"[ERROR] 시나리오 파일을 찾을 수 없습니다: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"[ERROR] 시나리오 파일의 형식이 올바르지 않습니다: {file_path}")
        return []

async def run_single_test(scenario):
    """개별 테스트 시나리오를 실행하고 결과를 출력합니다."""
    print("-" * 50)
    print(f"▶️  Scenario ID: {scenario['id']}")
    print(f"▶️  Description: {scenario['description']}")
    print(f"▶️  Expected: {scenario['expected_behavior']}")
    print("-" * 50)

    user_input = scenario['user_input']
    print(f"👤 User: {user_input}")

    # 시스템 프롬프트 및 대화 기록 생성
    # 테스트 목적에 맞게 성별, 모드 등은 기본값으로 설정
    system_prompt = build_system_prompt(gender="female", mode="banmal")
    history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    try:
        # LLM 응답 생성
        llm_response = await get_chatbot_response(history)
        print(f"🤖 LLM: {llm_response}")

    except Exception as e:
        print(f"[ERROR] LLM 응답 생성 중 오류가 발생했습니다: {e}")

    print("\n" + "="*50 + "\n")


async def main():
    """테스트베드 메인 실행 함수"""
    print("🚀 LLM 응답 테스트를 시작합니다...\n")
    scenarios_path = os.path.join(os.path.dirname(__file__), 'test_scenarios.json')
    scenarios = load_scenarios(scenarios_path)

    if not scenarios:
        print("실행할 테스트 시나리오가 없습니다.")
        return

    for scenario in scenarios:
        await run_single_test(scenario)

    print("✅ 모든 테스트 시나리오 실행이 완료되었습니다.")

if __name__ == "__main__":
    # Python 3.8+ on Windows: ProactorEventLoop is not compatible with subprocesses.
    # Use a different policy if you encounter issues.
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())

