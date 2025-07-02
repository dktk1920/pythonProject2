import json
import os
import csv
# from openai import OpenAI # OpenAI API 사용 시 주석 해제
# import google.generativeai as genai # Gemini API 사용 시 주석 해제

# --- 설정 --- #

# 사용할 LLM 타입과 모델 설정
# "openai" 또는 "gemini" 중 선택
LLM_TYPE = "openai" 
# OpenAI 모델: "gpt-3.5-turbo", "gpt-4" 등
# Gemini 모델: "gemini-pro" 등
LLM_MODEL = "gpt-3.5-turbo"

# --- LLM 호출 함수 (시뮬레이션 또는 실제 API) --- #
def call_llm(prompt: str, llm_type: str = LLM_TYPE, model: str = LLM_MODEL) -> str:
    """
    LLM (OpenAI 또는 Gemini) 호출을 시뮬레이션하거나 실제 API를 호출하는 함수.
    실제 사용 시에는 해당 LLM API 호출 코드를 활성화합니다.
    """
    print(f"\n--- LLM 호출 (LLM: {llm_type}, 모델: {model}) ---")
    print(f"프롬프트: {prompt.strip()}")

    # --- 실제 LLM API 호출 예시 (주석 해제 후 사용) ---
    # if llm_type == "openai":
    #     if not OPENAI_API_KEY: return "오류: OpenAI API 키가 설정되지 않았습니다."
    #     try:
    #         client = OpenAI(api_key=OPENAI_API_KEY)
    #         response = client.chat.completions.create(
    #             model=model,
    #             messages=[{"role": "user", "content": prompt}]
    #         )
    #         return response.choices[0].message.content
    #     except Exception as e:
    #         return f"OpenAI API 호출 오류: {e}"
    # elif llm_type == "gemini":
    #     if not GEMINI_API_KEY: return "오류: Gemini API 키가 설정되지 않았습니다."
    #     try:
    #         genai.configure(api_key=GEMINI_API_KEY)
    #         model_gemini = genai.GenerativeModel(model)
    #         response = model_gemini.generate_content(prompt)
    #         return response.text
    #     except Exception as e:
    #         return f"Gemini API 호출 오류: {e}"

    # --- 시뮬레이션된 응답 (API 호출 주석 처리 시 사용) ---
    if "힘들었어" in prompt:
        return "정말 힘든 하루였군요. 괜찮아요. 제가 옆에 있어요."
    elif "만점 받았어" in prompt:
        return "와! 정말 대단해요! 축하합니다!"
    elif "화가 나" in prompt:
        return "화가 많이 나셨군요. 어떤 일 때문에 그러신가요?"
    elif "기대돼요" in prompt:
        return "새로운 시작에 대한 기대감이 느껴지네요! 응원합니다."
    elif "불안해요" in prompt:
        return "불안한 마음이 드시는군요. 어떤 점이 가장 걱정되시나요?"
    elif "날씨가 너무 좋아서" in prompt:
        return "화창한 날씨가 기분을 좋게 하는군요! 즐거운 하루 보내세요."
    elif "업무 스트레스" in prompt:
        return "업무 스트레스가 많으시군요. 잠시 쉬어가며 마음을 다독이는 건 어떨까요?"
    elif "친구가 나를 배신했어" in prompt:
        return "친구가 배신해서 많이 속상하고 화가 나셨겠어요. 힘내세요."
    else:
        return "죄송합니다. 이해하지 못했습니다. (시뮬레이션 응답)"

# --- 결과 저장 함수 --- #
def save_results_to_file(results: dict, filename: str = "experiment_results", file_format: str = "csv"):
    """
    실험 결과를 파일로 저장하는 함수.
    :param results: 실험 결과 딕셔너리
    :param filename: 저장할 파일 이름 (확장자 제외)
    :param file_format: 저장할 파일 형식 ("csv" 또는 "txt")
    """
    full_filename = f"{filename}.{file_format}"
    if file_format == "csv":
        with open(full_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["case_id", "input", "emotion", "persona", "generated_prompt", "llm_response", "expected_response", "match_expected"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for case_id, data in results.items():
                writer.writerow({
                    "case_id": case_id,
                    "input": data["input"],
                    "emotion": data["emotion"],
                    "persona": data["persona"],
                    "generated_prompt": data["generated_prompt"],
                    "llm_response": data["llm_response"],
                    "expected_response": data.get("expected_response", ""), # 기대 응답이 없을 경우 빈 문자열
                    "match_expected": data.get("match_expected", "") # 일치 여부가 없을 경우 빈 문자열
                })
        print(f"\n결과가 {full_filename} (CSV) 파일로 저장되었습니다.")
    elif file_format == "txt":
        with open(full_filename, 'w', encoding='utf-8') as txtfile:
            for case_id, data in results.items():
                txtfile.write(f"========================================\n")
                txtfile.write(f"테스트 케이스 {case_id}\n")
                txtfile.write(f"  입력: {data['input']}\n")
                txtfile.write(f"  감정: {data['emotion']}\n")
                txtfile.write(f"  페르소나: {data['persona']}\n")
                txtfile.write(f"  생성된 프롬프트:\n{data['generated_prompt'].strip()}\n")
                txtfile.write(f"  LLM 응답: {data['llm_response']}\n")
                if "expected_response" in data:
                    txtfile.write(f"  기대 응답: {data['expected_response']}\n")
                    txtfile.write(f"  기대 응답 일치: {data['match_expected']}\n")
                txtfile.write(f"========================================\n\n")
        print(f"\n결과가 {full_filename} (TXT) 파일로 저장되었습니다.")
    else:
        print("지원하지 않는 파일 형식입니다. (csv 또는 txt)")

# --- 메인 실험 함수 --- #
def run_experiment(save_to_file: bool = False, output_filename: str = "experiment_results", output_format: str = "csv"):
    """
    감정/연령대별 프롬프트 실험을 실행하는 메인 함수.
    :param save_to_file: 결과를 파일로 저장할지 여부 (True/False)
    :param output_filename: 저장할 파일 이름 (확장자 제외)
    :param output_format: 저장할 파일 형식 ("csv" 또는 "txt")
    """
    # test_cases.json 로드
    try:
        with open('test_cases.json', 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
    except FileNotFoundError:
        print("오류: test_cases.json 파일을 찾을 수 없습니다. testbed 디렉토리에 있는지 확인해주세요.")
        return

    # prompt_template.json 로드
    try:
        with open('prompt_template.json', 'r', encoding='utf-8') as f:
            prompt_templates = json.load(f)
    except FileNotFoundError:
        print("오류: prompt_template.json 파일을 찾을 수 없습니다. testbed 디렉토리에 있는지 확인해주세요.")
        return

    all_results = {}

    for case in test_cases:
        case_id = case['id']
        input_text = case['input']
        emotion = case['emotion']
        persona = case['persona']
        expected_response = case.get('expected_response', None) # 기대 응답 로드

        print(f"\n========================================")
        print(f"테스트 케이스 {case_id}\n")
        print(f"  입력: {input_text}\n")
        print(f"  감정: {emotion}\n")
        print(f"  페르소나: {persona}\n")
        if expected_response: print(f"  기대 응답: {expected_response}\n")
        print(f"========================================")

        # 해당 페르소나와 감정에 맞는 프롬프트 템플릿 찾기
        generated_prompt = ""
        if persona in prompt_templates and emotion in prompt_templates[persona]:
            template_string = prompt_templates[persona][emotion]
            # 입력 문자를 프롬프트 템플릿에 삽입
            generated_prompt = template_string.format(input=input_text)
        else:
            # 적절한 템플릿이 없을 경우 기본 프롬프트 사용 또는 오류 처리
            generated_prompt = f"다음 질문에 답변해주세요: {input_text}"
            print(f"경고: {persona} - {emotion} 에 해당하는 프롬프트 템플릿을 찾을 수 없습니다. 기본 프롬프트를 사용합니다.")

        print(f"\n--- 생성된 프롬프트 ---")
        print(f"{generated_prompt.strip()}")

        # LLM 호출
        llm_response = call_llm(generated_prompt)
        print(f"LLM 응답: {llm_response}")

        # 기대 응답과 LLM 응답 비교
        match_expected = "N/A"
        if expected_response:
            match_expected = "일치" if llm_response.strip() == expected_response.strip() else "불일치"
            print(f"기대 응답 일치: {match_expected}")

        # 결과 저장
        all_results[case_id] = {
            "input": input_text,
            "emotion": emotion,
            "persona": persona,
            "generated_prompt": generated_prompt,
            "llm_response": llm_response,
            "expected_response": expected_response,
            "match_expected": match_expected
        }

    # 결과 요약 출력
    print("\n\n========================================")
    print("모든 실험 결과 요약")
    print("========================================")
    for case_id, data in all_results.items():
        print(f"\n테스트 케이스 {case_id} (입력: {data['input']}, 감정: {data['emotion']}, 페르소나: {data['persona']})")
        print(f"  생성된 프롬프트: {data['generated_prompt'].strip()[:70]}...") # 프롬프트가 길 경우 일부만 표시
        print(f"  LLM 응답: {data['llm_response']}")
        if data.get("expected_response"):
            print(f"  기대 응답: {data['expected_response']}")
            print(f"  기대 응답 일치: {data['match_expected']}")

    # 결과를 파일로 저장
    if save_to_file:
        save_results_to_file(all_results, output_filename, output_format)

# --- 스크립트 실행 --- #
if __name__ == "__main__":
    # 실험 실행
    # 결과를 파일로 저장하려면 save_to_file=True로 변경하고 output_filename, output_format 설정
    run_experiment(save_to_file=True, output_format="txt") # TXT 파일로 저장
    # run_experiment(save_to_file=True, output_filename="my_emotion_persona_experiment", output_format="csv") # CSV 파일로 저장
    # run_experiment(save_to_file=True, output_filename="my_emotion_persona_experiment", output_format="txt") # TXT 파일로 저장