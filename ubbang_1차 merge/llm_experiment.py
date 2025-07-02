import json
from prompt_template import PROMPT_TEMPLATE

def call_llm(prompt):
    # 이 함수는 실제 LLM API 호출을 시뮬레이션합니다.
    # 실제 사용 시에는 여기에 OpenAI, Gemini 등의 LLM API 호출 코드를 작성합니다.
    print(f"\n--- LLM 호출 시뮬레이션 ---")
    print(f"프롬프트: {prompt.strip()}")
    if "날씨" in prompt:
        return "오늘은 맑고 기온은 25도입니다."
    elif "음식" in prompt:
        return "저는 데이터로 이루어져 있어서 음식을 먹을 수 없습니다. 하지만 사람들이 좋아하는 음식은 다양하죠!"
    elif "인공지능" in prompt:
        return "인공지능은 인간의 학습 능력, 추론 능력, 지각 능력 등을 컴퓨터 프로그램으로 구현한 기술입니다."
    else:
        return "죄송합니다. 이해하지 못했습니다."

def run_experiment():
    with open('test_cases.json', 'r', encoding='utf-8') as f:
        test_cases = json.load(f)

    for case in test_cases:
        input_text = case['input']
        prompt = PROMPT_TEMPLATE.format(input=input_text)

        print(f"\n--- 테스트 케이스 {case['id']} ---")
        print(f"입력: {input_text}")
        print(f"생성된 프롬프트:\n{prompt.strip()}")

        llm_response = call_llm(prompt)
        print(f"LLM 응답: {llm_response}")

if __name__ == "__main__":
    run_experiment()
