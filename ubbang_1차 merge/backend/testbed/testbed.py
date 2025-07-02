import asyncio
import os
import json
import sys
from app.openai_helper import get_chatbot_response, build_system_prompt

async def test_persona_responses(persona, age_group):
    print(f"🎭 페르소나 테스트 시작: {persona['name']} ({persona['id']})")

    # openai_helper.py의 build_system_prompt에 personality와 age_group 전달
    system_prompt = build_system_prompt(personality=persona['description'], age_group=age_group)

    test_cases = persona.get('test_cases', [])
    if not test_cases:
        print("⚠️ 이 페르소나에 대한 테스트 케이스가 없습니다.")
        return

    for i, message in enumerate(test_cases, 1):
        print(f"\n🧪 [Test Case {i}]")
        print(f"👤 User ({persona['name']}): {message}")

        try:
            response = await get_chatbot_response(persona['id'], message, system_prompt)
            print(f"🤖 Response: {response}")
        except Exception as e:
            print(f"⚠️ 응답 실패: {e}")

    print(f"\n✅ 페르소나 테스트 완료: {persona['name']}\n")


def get_persona_files():
    # testbed 디렉토리로 경로 변경
    testbad_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(testbad_dir)
    return [f for f in os.listdir('.') if f.endswith('_personas.json')]

async def main():
    persona_files = get_persona_files()
    persona_map = {f.replace('_personas.json', ''): f for f in persona_files}

    if len(sys.argv) < 2 or sys.argv[1] not in persona_map:
        print("사용법: python testbed.py [페르소나 그룹]")
        print("사용 가능한 페르소나 그룹:")
        for group in persona_map.keys():
            print(f"- {group}")
        return

    selected_group = sys.argv[1]
    file_name = persona_map[selected_group]

    with open(file_name, 'r', encoding='utf-8') as f:
        personas = json.load(f)
        for persona in personas:
            await test_persona_responses(persona, selected_group)

if __name__ == "__main__":
    asyncio.run(main())
