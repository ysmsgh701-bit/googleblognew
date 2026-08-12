# 2026-07-27 야간 파이프라인 결과 — 발행 보류 (OAuth 토큰 만료)

> nightly-2026-07-27.log 파일이 실행 중인 nightly.ps1에 잠겨 있어(Device or resource busy)
> 같은 내용을 이 사이드카 파일에 기록함.

## 실행 요약

| 단계 | 결과 |
|---|---|
| 1. 중복 발행 가드 | 통과 — published/index.md에 2026-07-27 발행 이력 없음 |
| 2. 글감 선정 | batch01 축2 **#19 「40대에 AI 공부 시작하기」** (큐 최상단 2026-07-27 슬롯) |
| 3. writer | 완료 — content/drafts/2026-07-27-learning-ai-in-your-40s.md |
| 4. reviewer | **PASS** (수정 13건 적용 후) — content/reviewed/2026-07-27-learning-ai-in-your-40s.md (+ .review.md) |
| 5. editor-in-chief | **APPROVED** — content/approved/2026-07-27-learning-ai-in-your-40s.md (publish_mode: LIVE) |
| 6. 발행 | ❌ **실패 → 건너뜀 (자격증명 오류)** |
| 7. 기록 | published/index.md 미갱신(정상). QUEUE.md 14행 '발행 대기' 유지 |

## 각 단계 상세

**2. 글감 선정 근거**
축 순환상 #17(축3) → #18(축1) 뒤이므로 축2 차례. published/index.md 27행 및 QUEUE.md 22행의
2026-07-27 슬롯 권고("축2 우선 — #19 40대 AI 공부")와 일치. 큐 외 임의 선정 아님.

**4. reviewer 검수**
- 경험·수치 창작 **2건 발견·제거**
  - (a) published #4(AI 용어 정리)의 집필 동기를 발행본과 정반대로 서술한 대목 → 발행본 자구로 교체
  - (b) 4단계를 시간 순서로 지나왔다는 단정 → 발행 순서(#2 설치 7/09가 #4 용어 7/11보다 앞섬)와
        모순되어 "막힐 때마다 하나씩 넘은 벽의 목록"으로 재규정
- 미기재 수치(학습 기간·하루 학습 시간·나이·비용·사내 인원) 본문 등장 **0건**
- 자사 발행분과 자구가 완전히 겹치던 **6개소 재작성** (#6·#16·#17·#2). 각도 분리 성립 판정
- 내부링크 6/6 글자 단위 일치

**5. editor-in-chief 최종 편집**
- 제목 확정: **「40대 AI 공부 — 비개발자 재무 실무자가 넘은 벽 4가지」** (33자)
  - writer 원안('…코드 모르는 재무 실무자가 실제로 지나온 4단계')은 reviewer 수정 (b)로 본문이 바뀌면서
    제목-본문 불일치가 되어 대안 1안으로 강등
- 라벨: AI도구 / 클로드 코드 사용법 / 사무직 AI (기존 축2 체계 재사용, 신규 0건)
- meta_description 121자
- 내부링크 독립 재대조 **6/6 일치**, 유사 슬러그군 13종 개별 대조 — 오연결 0건
- **예약 링크백 회수 1/1** — QUEUE.md 29행 #17 예약 (c)
  ("통제의 위치가 숫자 확인에서 규칙 확인으로 올라간다"를 직무 변화 근거로)
- #19로의 신규 링크백 예약 5건 등록 (QUEUE.md)
- 운영자 사후 확인 요청 4건(전부 비차단, 1인칭 심리·판단·현재 운영 구성 서술. 수치 창작 0건)

## 6. 발행 실패 상세

```
명령: py -3.11 src/publish_blogger.py "content/approved/2026-07-27-learning-ai-in-your-40s.md"
오류: google.auth.exceptions.RefreshError:
      ('invalid_grant: Token has been expired or revoked.',
       {'error': 'invalid_grant', 'error_description': 'Token has been expired or revoked.'})
위치: src/publish_blogger.py:42  creds.refresh(Request())
```

**원인 추정: OAuth 리프레시 토큰 7일 만료 (2026-07-19 장애의 재발)**
- Google Cloud OAuth 클라이언트가 **'테스트(Testing)' 게시 상태**이면 리프레시 토큰이 발급 7일 후 만료됨
- 직전 재인증 흔적: `config/credentials/token.json.expired-2026-07-19` (2026-07-19)
- `token.json` 최종 갱신 성공: **2026-07-26 01:21** (7/19 재인증 + 7일 이내)
- 2026-07-27 01:00 갱신 실패 → **7일 주기와 정확히 일치**

**조치**
nightly_prompt.md 6항에 따라 발행을 건너뛰고 글은 `content/approved/`에 그대로 보존했습니다.
publish_blogger.py는 토큰 갱신 실패 시 브라우저 동의(`InstalledAppFlow.run_local_server`)가 필요한데
헤드리스 실행에서는 불가능 → **자동 복구 불가, 운영자 조치 필요**.

## 운영자 조치 안내

**(1) 오늘 글 발행하기 — 로컬 터미널에서 직접 실행**
```
cd "C:\Users\ysmsg\OneDrive\바탕 화면\Google blog"
py -3.11 src/publish_blogger.py "content/approved/2026-07-27-learning-ai-in-your-40s.md"
```
브라우저 동의창이 뜨고, 승인하면 그대로 발행됩니다.
동의창이 뜨지 않고 같은 오류가 나면 `config/credentials/token.json`을
`token.json.expired-2026-07-27`로 이름을 바꾼 뒤 다시 실행하세요.
발행 후 출력 JSON의 url을 published/index.md와 QUEUE.md 14행에 기록해야 합니다.

**(2) 재발 방지 (권장)**
Google Cloud Console → API 및 서비스 → **OAuth 동의 화면**에서 게시 상태를
**'테스트' → '프로덕션'으로 전환**하면 7일 만료가 사라집니다.
사용자 유형이 '외부'여도 본인 계정만 쓰는 비공개 앱이라 별도 검증 심사 대상이 아닙니다.
이 조치를 하지 않으면 **매주 같은 시각에 야간 파이프라인이 같은 이유로 멈춥니다.**

## 남은 상태
- 글은 `content/approved/2026-07-27-learning-ai-in-your-40s.md`에 발행 대기 상태로 보존
- published/index.md 미갱신 (발행 이력 없음이 정상)
- QUEUE.md 14행 상태: **발행 대기(approved, 2026-07-27 슬롯)**
- #19로의 신규 링크백 예약 5건과 #17 예약 (c) 회수 표기는 "발행 성공 시 유효" 단서를 달아 등록됨
