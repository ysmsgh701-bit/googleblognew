# 애드센스 승인 조사 노트 (2026-07-08)

## 핵심 결론
1. **승인 문턱이 높아졌다.** 2025~2026년 들어 심사가 까다로워지고 기간도 길어짐(평균 2~4주).
   "사유 없는 거절"과 "가치가 별로 없는 콘텐츠" 거절이 급증.
2. **AI 콘텐츠 자체는 금지가 아니다.** 구글 정책은 생산 방식이 아니라 품질을 본다.
   단, ① 사람 검수 없는 대량 발행(scaled content abuse) ② 어느 사이트에나 있을 법한
   일반론 요약 ③ 저자 정체성·경험 부재 — 이 3가지가 AI 사이트 거절의 실제 원인.
3. **우리의 무기 = E-E-A-T.** 실명·실직업(재무전문가) 저자 + 실제 실무 경험담은
   순수 AI 사이트가 절대 못 따라오는 차별화 요소. 페르소나 컨셉이 곧 승인 전략이다.

## 신청 전 체크리스트 (여러 후기 종합)
- 글 15~20편 이상, 각 1,500자(한글) 이상, 이미지/표 1개 이상
- 필수 페이지: 소개 / 개인정보처리방침 / 문의 — 3종 모두
- Search Console 색인 완료 상태에서 신청
- 짧은 글·인사글·테스트글 0편 (있으면 삭제 후 신청)
- 한 분야를 파고드는 구조 (잡블로그보다 전문 블로그가 유리)
- 2025년부터 신청 시 전화번호 인증 필수
- 운영 기간: 최소 1개월 이상 꾸준한 발행 이력 (몰아서 15편 X)

## "가치가 별로 없는 콘텐츠" 거절 대응
- 거절 원인: 짧고 피상적인 글, 정보 요약형 글(경험 없음), AI 원문 그대로, 복사/번역
- 대응: 거절 후 새 글 1~2편 추가하고 **즉시 재신청 가능** (재신청 제한 없음)
- 메인페이지 첫 문구·소제목을 메인 키워드와 통일

## 자동 발행 기술
- **Blogger API v3** (공식): Python `google-api-python-client` + OAuth 2.0.
  draft 업로드 / publish 모두 가능. → publisher 에이전트의 기반
- **티스토리**: 공식 Open API 종료. 브라우저 자동화로만 가능 → STEP 6에서

## 출처
- [애드센스 자격 요건 (구글 공식)](https://support.google.com/adsense/answer/9724?hl=ko)
- [블로그에 광고 게재하기 — Blogger 고객센터](https://support.google.com/blogger/answer/1269077?hl=ko)
- [애드센스 초단기 승인 방법 총정리 — 애드센스팜](https://adsensefarm.kr/google-adsense-ultra-short-term-approval-application-method/)
- [2026년 애드센스 승인 트렌드: 사유 없는 거절, 가치 없는 콘텐츠](https://weolbu.com/community/3932571/)
- [애드센스 승인 기간 (2026년 최신)](https://www.tmsystem.co.kr/4624)
- ["가치가 별로 없는 콘텐츠" 해결 방법 — 헨리프레스](https://henrypress.net/adsense-low-value-content-fix/)
- [승인 거절 대처방법 — 애드센스팜](https://adsensefarm.kr/adsense-reject-approval-how-to-deal-with-it/)
- [7차 도전 끝 승인 후기](https://richfreesia.com/entry/7%EC%B0%A8-%EB%8F%84%EC%A0%84-%EC%95%A0%EB%93%9C%EC%84%BC%EC%8A%A4-%EC%8A%B9%EC%9D%B8-%EC%82%AC%EC%9D%B4%ED%8A%B8-%EB%8B%A4%EC%9A%B4-%EA%B0%80%EC%B9%98%EA%B0%80-%EB%B3%84%EB%A1%9C-%EC%97%86%EB%8A%94-%EC%BD%98%ED%85%90%EC%B8%A0)
- [AdSense AI Content Policy 2026](https://adsenseaudit.net/guides/adsense-ai-content-policy-2026)
- [Is AI Content Allowed in Google AdSense?](https://hastewire.com/blog/is-ai-content-allowed-in-google-adsense-full-guide)
- [Blogger API Python 가이드 (Google)](https://developers.google.com/blogger/docs/1.0/developers_guide_python)
- [easyblogger — Python Blogger client](https://github.com/raghur/easyblogger)
- 참조 영상: [구글 블로그? '이거' 모르면 처음부터 애드센스 못 법니다](https://www.youtube.com/watch?v=Evi_codUi0s)
  (자막 API 차단으로 전문은 못 가져옴 — 제목상 블로거 애드센스 공략 영상, 필요 시 브라우저로 재시도)
