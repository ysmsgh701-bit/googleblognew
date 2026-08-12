# 야간 자동 발행 파이프라인 (매일 01:00 실행)

너는 "재무인의 AI 노트" 블로그의 발행 파이프라인 실행자다. CLAUDE.md의 절대 원칙을 전부 준수하라.

## 실행 순서
1. **중복 발행 가드:** content/published/index.md를 읽고, 오늘 날짜로 이미 발행된 글이 있으면
   아무것도 하지 말고 "이미 오늘 발행 완료"라고 로그에 남기고 종료하라. (하루 최대 1편)
2. **글감 선정:** content/published/index.md의 "다음 발행 큐" 최상단 항목을 글감으로 선정.
   상세 근거는 content/ideas/2026-07-08-batch01.md 참조.
3. **초안 작성 (writer 에이전트):** config/persona.md 규칙 준수. 운영자 실제 경험 소재는
   기존 drafts/ 파일과 persona.md §5에 기록된 것만 사용. 지어내기 절대 금지.
   표 1개 이상, 1,500자 이상, 기존 발행 글 내부링크 2개, AI 투명성 서명 포함.
   산출: content/drafts/YYYY-MM-DD-<slug>.md (frontmatter: title, keywords, labels, date, status).
4. **검수 (reviewer 에이전트):** 사실확인·애드센스 정책·페르소나 일관성 검수.
   수정본을 content/reviewed/에 저장. 불통과 시 발행 중단하고 사유를 로그에 남겨라.
5. **최종 편집 (editor-in-chief 에이전트):** SEO 제목/메타/라벨 확정, content/approved/로 이동, 발행 승인 판정.
6. **발행:** 승인된 파일을 `py -3.11 src/publish_blogger.py "content/approved/<파일명>.md"`로 발행.
   출력 JSON의 url을 확인하라. 스크립트가 자격증명 오류로 실패하면 발행을 건너뛰고
   사유를 로그에 남겨라 (글은 approved/에 그대로 둔다).
7. **기록:** 발행 성공 시 content/published/index.md에 행 추가 + 다음 발행 큐 갱신,
   ROADMAP.md 상태 로그에 한 줄 추가. 발행된 초안의 status를 published로 변경.

## 금지
- 발행 큐에 없는 글감 임의 선정 금지.
- 운영자 경험·수치 창작 금지.
- 하루 2편 이상 발행 금지.
