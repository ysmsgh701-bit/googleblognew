# CLAUDE.md — AI 재무전문가 블로그 · 애드센스 수익화 프로젝트

## 0. 프로젝트 한 줄 정의
**"AI를 공부하고 활용하는 40대 재무전문가"** 컨셉의 블로그를 구글 블로거(Blogger)에 만들고,
멀티 에이전트 파이프라인으로 글을 생산해 **애드센스 승인 → 수익화 → 티스토리 확장**까지 간다.

- 운영자: 회계/재무 실무자 (프로그래머 아님). 도메인 지식과 실제 경험 제공.
- Claude Code: 에이전트 파이프라인 구현, 자동화, 기술 작업 담당.
- 보고는 한국어, 코드/주석은 영어.

## 1. 절대 원칙 (애드센스 1회 실패 경험 반영)
1. **발행 게이트 = reviewer 검수.** (2026-07-08 운영자 결정으로 변경: 운영자 사전 확인 없이
   검수 통과 글은 자동 발행 가능. 단, 아래 조건 필수)
   - reviewer 체크리스트 전 항목 통과한 글만 발행
   - 운영자 경험 소재는 운영자가 제공한 내용만 사용 (지어내기 금지는 유지)
   - 발행 페이스: **매일 1편, 새벽 1시 자동 파이프라인 실행** (2026-07-12 운영자 결정으로
     주 3~5편 → 매일 1편으로 확대. 하루 최대 1편·대량 발행 금지 원칙은 유지)
   - 발행 후 published/index.md에 기록하고 운영자에게 URL 보고
2. **경험을 지어내지 않는다.** 글에 들어가는 사례·수치·경험담은 운영자의 실제 경험
   (재무 실무, Claude 자동화, 월마감 등)에서 나와야 한다. 없는 경험은 쓰지 않는다.
3. **모든 글에 운영자 고유의 관점 1개 이상.** 검색하면 나오는 정보 요약만으로 된 글은 발행하지 않는다.
4. **정책 위반 소재 금지:** 저작권 이미지, 의료/금융 과장 조언, 타 콘텐츠 복사·번역 짜깁기.
5. **원본 데이터(발행 이력, 초안)는 삭제하지 않는다.** content/ 아래에 전부 보관.

## 2. 블로그 컨셉
- 블로그명: **재무인의 AI 노트** — https://finance-ai-note.blogspot.com (필명: 재무인)
- 페르소나: 40대 현직 재무전문가. AI(Claude 등)를 실무에 직접 적용하며 배우는 과정을 기록.
- 콘텐츠 축 (3개 유지):
  1. **AI × 재무 실무** — 월마감/연결/엑셀 자동화 실전기 (최대 차별화 무기)
  2. **AI 도구 활용법** — 재무·사무직 관점의 Claude/GPT 활용 가이드
  3. **재무 지식** — 실무자가 풀어주는 회계/재무 개념
- 언어: 한국어 우선. (승인 후 영어 확장 검토)

## 3. 에이전트 파이프라인 (agents/)
| # | 에이전트 | 역할 | 산출물 |
|---|---------|------|--------|
| 1 | topic-scout | 글감 발굴: 검색 트렌드, 네이버/구글 키워드, 경쟁 글 분석 | 글감 후보 + 키워드 + 근거 |
| 2 | writer | 초안 작성: 페르소나 목소리, 운영자 경험 소재 반영 | 마크다운 초안 |
| 3 | reviewer | 검수: 사실확인, 애드센스 정책 체크, 표절/중복 검사 | 검수 리포트 + 수정본 |
| 4 | editor-in-chief | 최종 편집: SEO 제목/메타, 내부링크, 발행 판정 | 발행 승인/반려 |
| 5 | continuity | (추가) 연속성 관리: 발행 캘린더, 시리즈 연결, 내부링크 맵, 페르소나 일관성 | 발행 큐 |
| 6 | visual | (추가) 비주얼: 차트/다이어그램/썸네일 생성 (재무 글엔 표·차트 필수) | 이미지 파일 |
| 7 | publisher | 발행: 검수·편집 통과 글을 자동 publish (2026-07-08 운영자 결정. 애드센스 승인 전에도 적용 중) | 발행 결과 로그 |
| 8 | analyst | (승인 후) Search Console/애널리틱스 성과 분석 → topic-scout에 피드백 | 성과 리포트 |

파이프라인: topic-scout → writer → visual → reviewer → editor-in-chief → continuity(큐 배치) → publisher

## 4. 폴더 구조
```
Google blog/
├── CLAUDE.md            # 이 문서
├── ROADMAP.md           # 단계별 진행 현황 (체크박스)
├── docs/                # 조사 노트 (애드센스 정책 등)
├── config/
│   ├── persona.md       # 페르소나 정의 (말투, 금지 표현, 서명)
│   ├── settings.json    # Blogger blogId, 발행 규칙, 카테고리(라벨)
│   └── credentials/     # OAuth 토큰 (git 제외 대상)
├── content/
│   ├── ideas/           # 1. 글감 후보
│   ├── drafts/          # 2. 초안
│   ├── reviewed/        # 3. 검수 완료
│   ├── approved/        # 4. 발행 대기 큐
│   └── published/       # 5. 발행 완료 (발행일·URL 기록)
├── src/                 # 파이프라인 코드 (publish_blogger.py, nightly.ps1, nightly_prompt.md)
└── logs/                # 야간 자동 실행 로그
```

## 5. 실행 환경
- 이 PC의 기본 `python`은 다른 venv로 잡혀 있으므로 **반드시 `py -3.11` 사용**.
- Blogger 발행: `py -3.11 src/publish_blogger.py <approved 파일>` (Blogger API v3 + OAuth 2.0).
  최초 1회 `config/credentials/client_secret.json` 필요 (Google Cloud Console에서 데스크톱 앱
  OAuth 클라이언트 생성 + Blogger API v3 활성화). 이후 token.json 자동 갱신.
- 야간 자동 발행: Windows 작업 스케줄러 `FinanceAINote-Nightly`가 매일 01:00에
  `src/nightly.ps1` 실행 → Claude Code 헤드리스(`-p`, acceptEdits + .claude/settings.json
  허용 목록)로 `src/nightly_prompt.md` 파이프라인 수행. 로그: `logs/nightly-YYYY-MM-DD.log`.
- 티스토리: 공식 Open API가 종료되어 자동 발행은 브라우저 자동화 필요 → 2단계에서 다룬다.

## 6. 진행 방식
- 한 번에 전부 만들지 않는다. ROADMAP.md의 단계를 하나씩 완료하고 확인받는다.
- 애드센스 신청 타이밍 등 전략 판단은 운영자가 결정, Claude는 근거를 제시한다.
