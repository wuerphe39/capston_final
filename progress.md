# 프로젝트 진행 현황
> AI 기반 반려견 짖음 감지 및 보호자 영상 출력 시스템
> 마지막 업데이트: 2026-04-21

---

## 현재 완료된 작업

### 1단계: 짖음 감지 모듈 (✅ 완료)

| 파일 | 역할 | 상태 |
|------|------|------|
| `main.py` | 전체 파이프라인 진입점, 감지 루프 | ✅ |
| `config.py` | 샘플레이트·임계값·키워드 설정 | ✅ |
| `detector/audio_stream.py` | 마이크 실시간 오디오 스트리밍 | ✅ |
| `detector/yamnet_model.py` | YAMNet 기반 짖음 감지 모델 | ✅ |
| `requirements.txt` | 의존성 패키지 정의 | ✅ |
| `.gitignore` | venv, __pycache__ 제외 설정 | ✅ |

#### 구현 내용 상세

**`config.py`**
- `SAMPLE_RATE = 16000` — YAMNet 요구 샘플레이트
- `CHUNK_DURATION = 1.0` — 1초 단위로 오디오 분석
- `BARK_THRESHOLD = 0.3` — 짖음 판정 임계값
- `BARK_KEYWORDS = ["dog", "bark", "yip", "howl", "bow-wow"]` — 감지 대상 클래스

**`detector/audio_stream.py` — `AudioStream` 클래스**
- `sounddevice.InputStream`으로 마이크 실시간 수집
- 콜백 방식으로 오디오를 `queue.Queue`에 적재
- `read()` 호출 시 다음 청크를 블로킹 방식으로 반환

**`detector/yamnet_model.py` — `BarkDetector` 클래스**
- TensorFlow Hub에서 YAMNet 모델 로드
- GitHub에서 클래스 맵(CSV) 다운로드 후 짖음 관련 인덱스 필터링
- `predict(waveform)` → `(is_bark, score, label)` 반환

**`main.py`**
- `AudioStream` + `BarkDetector` 연결
- 쿨다운 3초 — 짖음 감지 후 3초 이내 재감지 억제
- 짖음 감지 시 클래스명·점수 출력, 대기 중에는 현재 상태를 한 줄로 갱신

---

## 아직 구현되지 않은 단계

| 단계 | 내용 | 예정 폴더 |
|------|------|-----------|
| 2단계 | ElevenLabs TTS API 연동 (보호자 목소리 클로닝) | `tts/elevenlabs_tts.py` |
| 3단계 | D-ID 얼굴 합성 API 연동 (사진 + 음성 → 영상) | `avatar/did_avatar.py` |
| 4단계 | 전체 파이프라인 통합 + 디스플레이 출력 | `ux/` |
| 5단계 | 테스트·최적화·발표 준비 | — |

---

## 시스템 흐름 (현재 구현 범위)

```
🎙️ 마이크 입력  →  🐕 YAMNet 짖음 감지  →  터미널 출력
                      ↑___________________|  (쿨다운 3초)
```

최종 목표 흐름:
```
🎙️ 마이크  →  YAMNet 감지  →  멘트 결정
                                    ↓              ↓
                             ElevenLabs TTS    효과음 즉시 재생
                                    ↓
                               D-ID 얼굴 합성
                                    ↓
                            📺 보호자 영상 출력
```

---

## 의존성 패키지

```
tensorflow>=2.13.0
tensorflow-hub>=0.14.0
sounddevice>=0.4.6
numpy>=1.24.0
scipy>=1.11.0
```

---

## GitHub

- 저장소: https://github.com/wuerphe39/capston_final
- 브랜치: `main`
- 첫 커밋(Initial commit): 2026-04-21
  - 업로드 파일: main.py, config.py, requirements.txt, .gitignore, README.md, project.md, detector/

---

## 다음 할 일

1. ElevenLabs API 키 발급 및 `tts/elevenlabs_tts.py` 작성
2. D-ID API 키 발급 및 `avatar/did_avatar.py` 작성
3. 짖음 감지 시 TTS → D-ID 순서로 파이프라인 연결
4. 디스플레이 출력 모듈(`ux/`) 구현
