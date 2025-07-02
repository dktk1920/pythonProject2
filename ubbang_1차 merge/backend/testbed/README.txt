감성 챗봇 프롬프트 실험 시스템

파일 구성

- `prompt_experiment.py` : 실험 메인 스크립트 (LLM 호출, 결과 csv 저장)
- `test_cases.json` : 테스트 케이스 정의 (`input`, `persona`, `emotion`, `expected` 등)
- `prompt_template.json` : 감정/연령대별 프롬프트 지시어 모음
- `experiment_results.csv` : 실험 결과 자동 저장 파일 (자동 생성)
- `simple_evaluator.py` : 결과 csv 평가 스크립트 (option)
- `experiment_eval.csv` : 자동 평가 결과 파일 (자동 생성)

---

실행법

1. (환경설정)
   OpenAI API 키를 환경변수로 등록 (선택 사항, `prompt_experiment.py` 내 시뮬레이션 모드 사용 시 불필요)
   
   # Linux/macOS
   export OPENAI_API_KEY=sk-xxx...
   # Windows (명령 프롬프트)
   set OPENAI_API_KEY=sk-xxx...
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="sk-xxx..."
   

2. (테스트 실행)
   `prompt_experiment.py` 스크립트가 있는 디렉토리로 이동하여 실행합니다.
   현재 프로젝트 구조상 `backend/testbed` 디렉토리에서 실행해야 합니다.

   터미널에서
   python prompt_experiment.py
  
   실험 결과가 콘솔에 출력되며, `experiment_results.csv`로 자동 저장됩니다.
   (스크립트 내 `run_experiment` 함수의 `save_to_file` 인자를 `True`로 설정하면 파일 저장이 활성화됩니다.)

3. (자동 평가)
   python simple_evaluator.py

   평가 결과가 `experiment_eval.csv`로 저장됩니다.