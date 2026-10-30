# 공개 자료 검토와 설계 결정

검토일: 2026-10-31 (한국 시간). **29개 저장소를 비교 후보로 확인했고, 그중 관련 본문을 골라 읽었습니다.** 모든 파일을 정독하거나 모든 스킬을 설치·실행한 성능 비교는 아닙니다. 실제 개선본 실행 결과는 [검증 기록](VALIDATION.md)에 따로 적었습니다.

## 무엇을 기준으로 골랐나

대회 이름과 최신순 검색만으로 선택하지 않았습니다. Cofa·하이닉스 키워드, 범용 Codex 작업 방법, 공식 형식 안내, 후보가 밝힌 상위 원본으로 범위를 넓혔습니다. 같은 계열의 복제·재포장은 독립적인 개선 아이디어로 중복 계산하지 않았습니다.

판단 기준은 **현재 과제와의 관련성, 기본 개념을 이해하게 하는 설명, 작업 중 불필요한 대기, 기존 결과 보존, 검증 근거, 설치·유지 부담, 출처와 사용 조건**입니다. 최근 업데이트와 별 수는 후보 발견에 참고할 수 있지만 품질 점수로 사용하지 않았습니다. 각 후보의 실제 확인 경로와 파일 식별값은 [출처 목록](research-sources.json)에 있습니다.

- **본문 검토:** 아래에 지정한 지침의 관련 내용을 읽었습니다. 저장소 전체 감사라는 뜻은 아닙니다.
- **부분 검토:** 큰 문서에서 관련 절·도입부·목차를 확인했습니다.
- **소개 검토:** README의 소개·구성과 연결만 확인했습니다. 구현·동작은 검증하지 않았습니다.
- 외부 설치기, MCP 서버, 훅은 실행하지 않았습니다.

## 대회 환경과 가까운 후보

| 후보 | 확인 범위 | 얻은 판단과 채택 범위 |
| --- | --- | --- |
| [ColdTbrew/cofa-skills](https://github.com/ColdTbrew/cofa-skills) | README, data-audit·requirements-elicitation·verify-before-submit 본문, LICENSE·NOTICE | 자료의 의미와 결과를 바꿀 업무 정의를 확인하는 일부 절차를 개작. 학습 전제·자동 열 제외·필수 별도 기록은 가져오지 않음. |
| [JINwonLEE/cofa-codex-harness](https://github.com/JINwonLEE/cofa-codex-harness) | README, hx-debug·hx-interview 본문, LICENSE·NOTICE | 재현→근거 확인→최소 수정과 필요한 질문을 고르는 절차를 개작. 고정 조사 시간·매번 커밋·명시 호출 전용은 가져오지 않음. |
| [ripplelover/cofa-ready-kit](https://github.com/ripplelover/cofa-ready-kit) | README, cofa-triage·cofa-explain 본문 | 시작점 하나와 평소 문장으로 진행하는 방식 비교. 전체 도구 설치나 특정 도메인 전제는 적용하지 않음. |
| [B0neh3ad/cofa-toolkit](https://github.com/B0neh3ad/cofa-toolkit) | README, domain-discovery·explain-artifact 본문 | 개념과 입력·출력을 연결하는 설명 비교. 큰 도구 묶음과 모든 연습을 기본 설치에 넣지 않음. |
| [jincode93/cofa-kit](https://github.com/jincode93/cofa-kit) | README 소개 검토 | 계획·결정·검증·작업 기록 구조 비교. 모든 문서를 매번 만들거나 Git 설정을 자동 변경하는 구성은 채택하지 않음. |
| [allsleep7610/hynix-hackathon-workflow](https://github.com/allsleep7610/hynix-hackathon-workflow) | README, my-communication·my-feature-guide 본문 | 사용자 안내를 선택적 이해 활동으로 두고 AI가 검증하는 방식 비교. 다단계 검토·세션 체계 전체를 옮기지 않음. 본문 복사 없음. |
| [Kijan03/cofa-prove-skill](https://github.com/Kijan03/cofa-prove-skill) | README 관련 부분 | 데이터·로그·탐색 분석 도구 후보. 해당 입력이 있을 때 검토할 도구이며 범용 스킬의 필수 의존성으로 넣지 않음. |
| [zittenyetten/cofa-probe-kit](https://github.com/zittenyetten/cofa-probe-kit) | README, task-evidence-check 본문 | 실제 과제와 키트 안내의 구분, 한 중심 지침과 조건부 참조 구조 비교. 현재 증거를 우선하는 설계에 참고. |
| [arcturus0637-rgb/cofa-prelim-kit](https://github.com/arcturus0637-rgb/cofa-prelim-kit) | README, cofa-concise·cofa-verify 본문 | 짧은 설명의 조건과 실행 근거·제외 항목 구분 비교. 짧은 형식 때문에 개념을 생략하거나 전체 평가 도구를 상시 요구하지 않음. |
| [dogsa33/cofa-ready-kit](https://github.com/dogsa33/cofa-ready-kit) | README, cofa-explain 본문 | 확인한 explain 파일이 ripplelover 후보와 같은 Git blob 식별값. 별개의 설명 개선 근거로 중복 계산하지 않음. |
| [sjj5563/hx-rules](https://github.com/sjj5563/hx-rules) | README 없음, AGENTS.md 본문 | 계획·승인·Git 기록 중심 구성 비교. 매 단계 승인과 자동 저장소 초기화는 현재 작업 흐름에 도입하지 않음. |
| [youngmin3170/ai-task-toolkit](https://github.com/youngmin3170/ai-task-toolkit) | README 관련 부분, ZIP 내부 스킬은 미검토 | 지속 기록과 인계 구성을 확인. 스킬 본문·실행까지 검증한 후보로 취급하지 않음. |
| [Malrangbbobbi/hynix-harness-kit](https://github.com/Malrangbbobbi/hynix-harness-kit) | README 소개 검토 | 템플릿·초기화·시간 배분 구성 비교. 여러 수동 단계와 고정 시간표를 기본 절차로 채택하지 않음. |
| [hamjoon2003/sk-hynix-2nd-harness](https://github.com/hamjoon2003/sk-hynix-2nd-harness) | README 관련 부분 | 검사 통과·실패·검사 불가를 구분하는 설명 비교. 검사가 0개인데 통과했다고 말하지 않는 원칙에 참고. 스크립트 실행 없음. |
| [jungwon123/sk-ai-kit](https://github.com/jungwon123/sk-ai-kit) | README 관련 부분, handoff 본문 | 인계 내용과 데이터·앱 작업 범위 비교. 고정 개수 문서·커밋·모델 선택 규칙은 채택하지 않음. |
| [rupria/SK-AI-](https://github.com/rupria/SK-AI-) | README 없음, skill.md 도입부·관련 부분 | 모델별 역할·초기 구성 예를 확인. 고정 모델 배치를 현재 환경의 규칙으로 간주하지 않음. |
| [H4RUming/kit](https://github.com/H4RUming/kit) | README 도입부·목차 | 작업 폴더·기록·커밋을 포함한 키트 구성 비교. 기존 프로젝트를 바꾸는 초기화는 가져오지 않음. |
| [PKJthecreator/probe-kit](https://github.com/PKJthecreator/probe-kit) | README 없음, AGENTS.md 본문 | 사용자가 중요한 값을 이해하도록 드러내는 방식 비교. 고정 시간과 단계별 승인·커밋을 강제하지 않음. |
| [MunChanCHOI1/qualifier-skill](https://github.com/MunChanCHOI1/qualifier-skill) | README, skhynix-qualifier 본문 | 중심 지침+조건부 참조, 실제 규칙 우선 구조 비교. 원문 전체 복제 없이 목적에 맞는 구조를 자체 작성. |

## 범용 작업 방법과 공식 형식

| 후보 | 확인 범위 | 얻은 판단과 채택 범위 |
| --- | --- | --- |
| [openai/skills](https://github.com/openai/skills) | README | 검토 당시 폐기 안내와 openai/plugins 이동 경로 확인. 과거 카탈로그를 최신 공식 원본으로 단정하지 않음. |
| [openai/plugins](https://github.com/openai/plugins) | README | 현재 공식 묶음 구조 참고. 모든 플러그인을 설치해야 한다는 의미로 사용하지 않음. |
| [anthropics/skills](https://github.com/anthropics/skills) | README 소개·구성 | 스킬의 목적과 구성 예 비교. 다른 제품의 등록 방법을 Codex/Cofa에 그대로 적용하지 않음. |
| [obra/superpowers](https://github.com/obra/superpowers) | README 관련 부분, systematic-debugging·verification-before-completion 본문 | 원인 확인 후 수정, 실행 근거가 있는 완료 주장 비교. 모든 작은 요청에 전체 단계·검사·여러 에이전트를 요구하지 않음. |
| [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 큰 README의 도입부·목차 | 긴 작업에서 지속 기록의 이점 확인. 짧은 요청마다 여러 기록 파일과 훅을 추가하지 않음. |
| [NVIDIA/skills](https://github.com/NVIDIA/skills) | README 도입부·목차 | 분야별 전문 스킬 카탈로그 확인. GPU·로봇 등 해당 요구가 없는 과제의 기본 구성에는 제외. |
| [rohitg00/pro-workflow](https://github.com/rohitg00/pro-workflow) | README 도입부·목차 | 작업·메모리·연구 기능 묶음 확인. 다수 의존성과 전역 설정을 이번 기본 설치에 추가하지 않음. |
| [composio-community/awesome-codex-skills](https://github.com/composio-community/awesome-codex-skills) | README 도입부·목차 | 추가 후보를 찾는 색인. 목록 등재만으로 개별 스킬 품질이나 외부 연결의 필요성이 검증되지는 않음. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | README 도입부·목차, diagnosing-bugs 관련 부분 | 구체적인 실패와 관측을 출발점으로 삼는 방식 비교. 고정 가설 개수·모든 단계의 질문을 강제하지 않음. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | README 도입부·목차, incremental-implementation 관련 부분 | 작게 끝까지 동작하는 결과와 범위 보존 방식 비교. 매번 전체 검사·자동 커밋하는 규칙은 채택하지 않음. |

## 병행 개정본과의 통합

게시 직전 같은 저장소의 [병행 개정 커밋](https://github.com/bryan528c/data-mission-skills/commit/f2d005e6dbbe651f541044c5f3a5e7272d8e49b6)을 확인해 그 커밋 위에서 통합했습니다. 기존 파일 경로·라이선스·[25개 후보 비교 기록](REVIEW.md)·22개 미실행 행동 시나리오를 보존했습니다. 그 기록은 해당 개정 작업의 조사이며, 이번 29개 직접 조사에 단순 합산해 검토 수나 성능 검증 수를 부풀리지 않습니다.

저장되지 않은 편집기 내용과 디스크 파일의 차이, 규정의 시행일·적용 범위, 자료 추출 실패, 테스트 0개와 통과의 구분, 실제 모델 설정 확인을 보완했습니다. 겹치는 설명·오류·도구 문서는 기존 참조 경로 다섯 개로 합쳤습니다. 자동 선택과 현재 규칙을 우선하며, 후보 수·질문 수·실패 횟수를 고정하는 절차는 강제하지 않습니다.

## 최종 구성에 반영한 것

| 해결할 문제 | 이번 구성 |
| --- | --- |
| 절차만 있고 기본 개념이 빠짐 | 쉬운 뜻 → 현재 예 → 이유 → 행동. 필요한 용어만 설명하는 별도 참조. |
| 어떤 스킬을 불러야 하는지 사용자가 외워야 함 | 기존 이름 하나 유지. 과제 맥락의 평소 요청과 필요한 참조를 연결. 자동 선택 허용을 명시. |
| 결과 확인 안내가 다음 작업의 대기 조건이 됨 | AI가 가능한 확인을 수행. 사용자 확인은 필요한 항목만 남기고 독립적인 작업은 계속. |
| 여러 키트가 같은 계획·검증·기록을 반복 | 중심 SKILL.md와 내부 참조 5개. 현재 상황에 필요한 부분만 읽음. |
| 간결함 때문에 결과 위치와 이해가 사라짐 | 뜻·조건·근거·실제 경로를 보존하며 마지막에 표현과 파일을 함께 확인. |
| 설치한 본문만 있고 보조 지침이 빠짐 | 스킬 폴더 전체를 복사하는 선택 설치기. 충돌 시 기존 파일 보존. |

공식 형식·등록 안내는 [OpenAI 스킬 문서](https://learn.chatgpt.com/docs/build-skills)를 함께 확인했습니다. **자동 선택을 허용하는 설정과 Cofa에서 실제로 인식·선택되는지는 별개의 검증 항목**입니다.

직접 개작한 두 후보의 확인한 커밋과 라이선스·상위 저작권 고지는 [NOTICE](../skills/data-mission-partner/NOTICE.md)에 있습니다. 조사한 저장소 전체가 MIT이거나 재배포 가능하다고 주장하지 않습니다. 복사 권한을 확인하지 않은 자료는 비교 대상으로만 사용했습니다.
