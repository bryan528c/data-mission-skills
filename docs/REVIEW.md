# 통합 검토 기록 · v2

이 문서는 제작 검토용이다. 실제 과제를 푸는 Codex가 매번 읽을 자료가 아니다.

## 검토 범위

2026-10-31 기준. 최신순만 보지 않고 대회 키트 검색, 별 수 기준 검색, 범용 작업·데이터·보안·UI 스킬 검색, 공식 작성 문서, 원본에서 연결된 출처를 교차 확인했다. `cofa` 단독 검색의 분자/추천시스템 등 동명이의 결과와 관련 없는 유명 저장소는 제외했다. 별 수·업데이트 날짜를 성능 증거로 쓰지 않았다.

**외부 25개 저장소의 안내 또는 관련 파일을 열람했다.** 이 중 7개 저장소에서는 관련 SKILL.md 본문 10개를 추가 확인했다. 모든 저장소의 전체 파일을 정밀 감사하거나 실제 모델로 25개를 비교 실행한 것은 아니다. 요청 범위가 잘린 반환은 아래에 표시한다. 조회에 실패한 `forrestchang/andrej-karpathy-skills`, `K-Dense-AI/claude-scientific-skills`는 이 수에 포함하지 않았다.

추가로 사용자의 Work판 7개 파일 구조와 핵심 5개 문서, 이전 Chat판 ZIP의 운영·검증·설치 구성과 스킬5개를 비교했다. 공개 파일에는 개인 대화 원문이나 과제 원문을 넣지 않았다.

## 선택 기준

쉬운 뜻과 실제 사례가 있는가, 작업을 끊지 않는가, 필요한 경우만 적용되는가, 과제별 기준을 보존하는가, 실행 근거를 확인하는가, 설치/참조가 자기완결적인가, 마지막 가독성 정리가 있는가를 보았다. 가상의 수치 점수나 공식 평가 가산점을 붙이지 않았다.

## 후보별 읽은 범위와 판단

| 저장소 | 실제 열람 범위 | 유용한 관점 | 제외·제약 |
|---|---|---|---|
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | README 1–150 | 한 번 합의 뒤 작은 실행 단위로 진행; 개별 설치의 외부 참조 누락 경고 | 단계마다 커밋·25개 전체 설치는 채택하지 않음 |
| [HyeongiJeon/CodexHarness](https://github.com/HyeongiJeon/CodexHarness) | README 1–130 반환 범위 | 자료 크기별 처리와 실행 근거를 분리한 구조 | 여러 역할·모델 설정·Python 실행기는 추가하지 않음; 작성자 benchmark를 재검증한 것은 아님 |
| [zittenyetten/cofa-probe-kit](https://github.com/zittenyetten/cofa-probe-kit) | README 1–105 반환 범위 | 실제 과제와 키트 구분, 시작 문장 하나 | 다량 가이드·PDF·시연 사례를 매 작업에 넣지 않음 |
| [keepbridge-ui/probe-prep-skills](https://github.com/keepbridge-ui/probe-prep-skills) | README 1–70 반환 범위 | 중요한 질문, 쉬운 설명, 실제 흐름 안내 | 세 스킬 명시 호출과 반복 이해 확인을 기본으로 강제하지 않음 |
| [ccmct/cofa-kit](https://github.com/ccmct/cofa-kit) | README 전체 + skills/code-tour/SKILL.md 전체 | 파일·핵심 처리·확인 장소를 연결하는 코드 설명 | 웹 서버·파이썬 문법·질문4개·사용자검증을 모든 과제에 강제하지 않음 |
| [combe4259/hy-codex-kit](https://github.com/combe4259/hy-codex-kit) | README 1–100 | 상황별 도구 구분 | 많은 수동 호출명·고정 문서 갱신·모델 변경 전 무조건 압축은 채택하지 않음 |
| [sonjeongwons/skills](https://github.com/sonjeongwons/skills) | README 전체 | 사건별 지침 선택, 앞 단계로 돌아갈 때 상태 보존 | 다섯 필수 문서·전역 설치·시각별 정형 절차는 채택하지 않음 |
| [dtd11/skhynix-harness-2nd](https://github.com/dtd11/skhynix-harness-2nd) | README 전체 | 고정 버전·출처 보존, 검증 근거 재사용 | 여러 키트를 중첩 활성화하거나 매 턴 같은 보고 형식을 쓰지 않음 |
| [denny6389/cofa-hackathon-kit](https://github.com/denny6389/cofa-hackathon-kit) | README 전체 | 작은 기능과 실제 근거; 별도 폴더가 제출제외를 보장하지 않음 | 작은 기능마다 전후 승인받는 흐름은 사용자 선택일 때만 |
| [ksh0330/ex-harness](https://github.com/ksh0330/ex-harness) | README 전체 | 기존 스택·최소 변경·같은 실패 반복 방지 | 예제 앱·8개 스킬·설치기까지 가져오지 않음 |
| [H4RUming/kit](https://github.com/H4RUming/kit) | README 1–90 | 실패 출력 요약, 테스트0개와 성공의 구분 | 폴더 자동 이동·별도 도구 실행·고정 문서4개·매 조건 정지는 채택하지 않음 |
| [seongwon030/agent-skills](https://github.com/seongwon030/agent-skills) | README 전체 | 짧은 상태 메모와 검증 | 평가용으로 사용자 판단을 꾸미지 않음; 정해진 시간마다 새 세션·커밋을 강제하지 않음 |
| [Kijan03/cofa-prove-skill](https://github.com/Kijan03/cofa-prove-skill) | README 전체 | 원본 전체 출력보다 구조 요약, 큰 파일 분할 처리 | 실행 코드는 검토·복사하지 않음; 예측·대시보드 뼈대를 기본으로 만들지 않음 |
| [arcturus0637-rgb/cofa-prelim-kit](https://github.com/arcturus0637-rgb/cofa-prelim-kit) | README 1–95 | 기존 설치 상태 우선, 조건부 전문 지침 | 원본9개·CLI·증거 ID를 모두 관리하게 하지 않음; 저자의 환경 해석은 공식 규칙 아님 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | README 1–120 | 작고 조합 가능한 지침과 사용자 통제 | 자동 업데이트 플러그인·이슈관리 설치는 제외; 원문 스킬의 효과를 실측하지 않음 |
| [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | README 1–105 | 파일에 중요한 상태를 남기는 개념 | 매 턴 Hook·세 개 필수 문서·자체 benchmark의 일반화는 제외 |
| [anthropics/skills](https://github.com/anthropics/skills) | skills/skill-creator/SKILL.md 1–165 | 사용자의 용어 이해도·실제 요청별 검토·필요할 때 참조 | Claude 실행·외부 평가 도구를 대회에 설치하지 않음 |
| [openai/skills](https://github.com/openai/skills) | skills/.system/skill-creator/SKILL.md 1–165 + references/openai_yaml.md 전체 | 명확한 적용 조건, 자기완결적인 참조, 적절한 자유도 | 등록 형식 검사와 실제 응답 검증을 구분 |
| [openai/plugins](https://github.com/openai/plugins) | data-analytics의 index 및 analyze-data-quality SKILL.md 반환 범위 | 한 행 의미·자료 품질·작업에 맞는 검사 | Chat/Work 전환 강제, 연결 계정 선택, 자동 게시 등 호스트 전용 절차는 제외 |
| [obra/superpowers](https://github.com/obra/superpowers) | skills/verification-before-completion/SKILL.md 전체 | 실제 근거를 보고 완료 판단 | 변경 없는 확인 답변에도 전체 검사를 새로 실행하는 강제 절차는 채택하지 않음 |
| [trailofbits/skills](https://github.com/trailofbits/skills) | README 1–115 | 변경·사양·검증 관점을 나눠 보는 전문 검사 후보 | 보안 감사 전부·추가 분석 도구를 일반 데이터 과제에 기본 적용하지 않음 |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | README 1–115 | 필요한 웹/UI 작업에 한정된 전문 규칙 | React·Vercel·100개 UI 규칙을 분석 과제 전체에 이식하지 않음 |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | README 1–100 | 공식 배포 경로·중복 설치 경고만 1차 확인 | 소개 구간만 읽음. 내부 스킬 품질·성능 판단 대상으로 사용하지 않음 |
| [ColdTbrew/cofa-skills](https://github.com/ColdTbrew/cofa-skills) | 고정 commit의 data-audit, verify-before-submit SKILL.md 전체 | 자료 의미·실제 실행 결과 검증을 v1에서 이어 개작 | 모든 과제의 모델학습·자동 열제외·각 단계 전체검사 강제는 제외 |
| [JINwonLEE/cofa-codex-harness](https://github.com/JINwonLEE/cofa-codex-harness) | 고정 commit의 hx-debug, hx-interview SKILL.md 전체 | 재현·최소 수정·결과를 바꾸는 질문을 v1에서 이어 개작 | 고정 인터뷰 라운드·여러 문서·매 수정 커밋은 제외 |

## 두 기존 묶음을 합친 방식

| 기준 | 기존 Chat판 | 기존 Work판 | 이번 기준본 |
|---|---|---|---|
| 사용 진입 | 5개 스킬, 각 implicit=false | 한 스킬, 자동선택 정책 미기재(일반 기본값은 true) | 한 스킬 유지, true 명시, 시작 한번 뒤 상황별 참조 선택 |
| 설명 | 짧은 4줄 보고 중심 | 이유·입출력 설명 원칙 | 기초 뜻→실제 한 사례→이유→확인 위치; 짧게 만들며 기초를 빼지 않음 |
| 진행 | 단계별 승인의 여지 | 일반 작업 자율 진행 | 계획만/실행 승인/단계별 확인 요청을 구분. 보고와 승인 대기를 구별 |
| 상세 기준 | 이름별 별도 설치 | 자료·마무리 참조2개 | 자기완결적인 참조5개로 정리; 필요할 때만 읽음 |
| 마지막 정리 | 검증·제출 중심 | 필수 결과 확인 | 내용 정확성 뒤 목적·이유·확인 동선·중복·가독성 한 번 다듬고 종료 |

모든 요구를 한꺼번에 읽게 하는 대형 지침으로 합치지 않았다. 모든 기존 스킬을 자동 활성화하는 것도 아니다. 본문에 어떤 상황에서 어느 참조를 읽을지 두고, 사람이 스킬 이름을 골라 입력하는 부담을 없앴다. 자동 적용은 모델의 지침 수행이며 실제 호스트 발견과 항상 준수를 보장하지 않는다.

## 출처와 테스트 경계

직접 복제·개작한 부분은 이전 v1의 ColdTbrew/JINwonLEE 두 MIT 출처로 한정하며 NOTICE와 스킬 내부 licenses를 유지한다. 다른 후보에서는 작업 원칙을 비교했고 실행 코드·스킬 원문을 추가 복사하지 않았다.

형식 검사 통과는 자동 선택·설명 품질·시간 절약의 실측이 아니다. 구조 검사와 행동 검토 시나리오를 구분하고, 실제 모델 실행은 미검증으로 남겼다. 상세는 VALIDATION.md를 본다.

공식 기술 참고:
- https://learn.chatgpt.com/docs/build-skills
- https://developers.openai.com/blog/eval-skills
- https://github.com/openai/skills/tree/main/skills/.system/skill-creator
