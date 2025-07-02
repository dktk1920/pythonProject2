import asyncio
import json
import os
import sys
from dotenv import load_dotenv

# --- 환경 변수 및 경로 설정 ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dotenv_path = os.path.join(project_root, '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"[ERROR] .env 파일을 찾을 수 없습니다: {dotenv_path}")
    sys.exit(1)

sys.path.insert(0, project_root)

from app.openai_helper import get_chatbot_response, build_system_prompt

# --- 데이터 로딩 함수 ---
def load_json_data(file_path):
    """범용 JSON 파일 로더"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] 파일을 찾을 수 없습니다: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"[ERROR] 파일의 형식이 올바르지 않습니다: {file_path}")
        return None

# --- 테스트 실행 로직 ---
async def run_test_for_persona(persona, scenarios):
    """하나의 페르소나에 대해 모든 시나리오를 테스트합니다."""
    print("\n" + "="*70)
    print(f"🧪 페르소나 테스트 시작: {persona['name']}")
    print("="*70)

    for scenario in scenarios:
        print("\n" + "-" * 50)
        print(f"▶️  시나리오: {scenario['description']} ({scenario['id']})")
        print(f"👤  사용자 입력: {scenario['user_input']}")
        print(f"🎯  기대 동작: {scenario['expected_behavior']}")
        print("-" * 50)

        # 이 페르소나의 프롬프트를 시스템 프롬프트로 설정
        # gender와 mode는 persona 객체에 직접 포함되어 있지 않으므로, 임시로 "female", "banmal" 사용
        # 실제 테스트 시에는 persona 객체에 gender와 mode 정보가 포함되어야 합니다.
        system_prompt = build_system_prompt(gender="female", mode="banmal") # TODO: persona에서 gender, mode 추출
        
        try:
            llm_response = await get_chatbot_response(pk="test_user", user_input=scenario['user_input'], system_prompt=system_prompt)
            print(f"🤖  LLM 응답 ({persona['name']}): {llm_response}")

        except Exception as e:
            print(f"[ERROR] LLM 응답 생성 중 오류: {e}")
        
        # 결과 구분을 위해 잠시 대기
        await asyncio.sleep(1)

async def main():
    """테스트베드 메인 실행 함수"""
    print("🚀 모든 페르소나에 대한 LLM 응답 테스트를 시작합니다...\n")

    testbad_dir = os.path.dirname(__file__)
    scenarios_path = os.path.join(testbad_dir, 'test_scenarios.json')
    scenarios_data = load_json_data(scenarios_path)

    if not scenarios_data:
        print("시나리오 데이터를 불러오는 데 실패했습니다.")
        return

    scenarios = scenarios_data.get("scenarios", [])

    # 나이대별 페르소나 파일 목록
    persona_files = [
        "teen_personas.json",
        "adult20_personas.json",
        "adult30_personas.json",
        "adult40_personas.json",
        "adult50_personas.json",
        "adult60_personas.json"
    ]

    for file_name in persona_files:
        personas_path = os.path.join(testbad_dir, file_name)
        personas_data = load_json_data(personas_path)

        if personas_data:
            for persona in personas_data:
                await run_test_for_persona(persona, scenarios)
        else:
            print(f"경고: {file_name} 파일을 불러오지 못했습니다. 이 파일의 테스트는 건너뜁니다.")

    print("\n" + "✅ 모든 페르소나 테스트가 완료되었습니다.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())