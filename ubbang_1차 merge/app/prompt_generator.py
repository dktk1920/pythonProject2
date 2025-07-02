import json

def generate_prompt(persona_id: str, scenario_id: str, personas_file_path: str, scenarios_file_path: str) -> str:
    """
    주어진 페르소나 ID와 시나리오 ID를 기반으로 동적 프롬프트를 생성합니다.
    """
    

    persona_description = ""
    user_input_for_scenario = ""

    # 페르소나 데이터 로드
    try:
        with open(personas_file_path, 'r', encoding='utf-8') as f:
            personas = json.load(f)
            for persona in personas:
                if persona['id'] == persona_id:
                    persona_description = persona['description']
                    break
    except FileNotFoundError:
        return f"Error: Persona file not found at {personas_file_path}"
    except json.JSONDecodeError:
        return f"Error: Could not decode JSON from {personas_file_path}"

    # 시나리오 데이터 로드
    try:
        with open(scenarios_file_path, 'r', encoding='utf-8') as f:
            scenarios_data = json.load(f)
            for scenario in scenarios_data.get('scenarios', []):
                if scenario['id'] == scenario_id:
                    user_input_for_scenario = scenario['user_input']
                    break
    except FileNotFoundError:
        return f"Error: Scenario file not found at {scenarios_file_path}"
    except json.JSONDecodeError:
        return f"Error: Could not decode JSON from {scenarios_file_path}"

    if not persona_description:
        return f"Error: Persona with ID '{persona_id}' not found."
    if not user_input_for_scenario:
        return f"Error: Scenario with ID '{scenario_id}' not found."

    # 프롬프트 조합
    # 여기서는 간단하게 페르소나 설명과 사용자 입력을 결합합니다.
    # 실제 LLM 프롬프트는 더 복잡하게 구성될 수 있습니다.
    dynamic_prompt = f"{persona_description}\n\n사용자 입력: {user_input_for_scenario}"

    return dynamic_prompt

if __name__ == "__main__":
    # 예시 사용
    # teen_01 페르소나 (고민 많은 중학생)와 scenario_01 (우울감 표현) 조합
    prompt = generate_prompt("teen_01", "scenario_01")
    print("--- Generated Prompt ---")
    print(prompt)

    print("\n--- Another Example ---")
    # teen_02 페르소나 (게임 덕후 고등학생)와 scenario_10 (긍정적인 경험 공유) 조합
    prompt_2 = generate_prompt("teen_02", "scenario_10")
    print(prompt_2)
