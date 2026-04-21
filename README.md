# AI 기반 반려견 짖음 감지 및 보호자 영상 출력 시스템

> 강아지가 짖으면 보호자의 AI 클로닝 얼굴과 목소리로 반응하는 졸업작품 프로젝트

---

## 개요

마이크로 강아지 짖음을 실시간 감지하고, 보호자의 목소리(ElevenLabs TTS)와 얼굴(D-ID)을 AI로 합성해 디스플레이에 출력합니다.

| 항목 | 내용 |
|------|------|
| 짖음 감지 | Google YAMNet (로컬 실행) |
| 목소리 클로닝 | ElevenLabs API |
| 얼굴 합성 | D-ID API |
| 실행 환경 | 노트북 또는 라즈베리파이 + 마이크 + 디스플레이 |

---

## 시스템 흐름

```
🎙️ 마이크 입력
    ↓
🐕 YAMNet 짖음 감지 (로컬)
    ↓ 짖음 감지 시
💬 멘트 결정 (짖음 패턴별 텍스트)
    ↓                    ↓
🔊 즉시 효과음 재생     🎵 ElevenLabs TTS 음성 생성
    ↓                    ↓
🖼️ 보호자 사진 + 로딩  🎬 D-ID 얼굴 합성 영상 생성
    ↓                    ↓
📺 보호자 얼굴 + 목소리 영상 출력
```

---

## 디렉토리 구조

```
dog-care/
├── main.py                  # 전체 파이프라인 진입점
├── config.py                # 설정값 (샘플레이트, 임계값, 키워드)
├── requirements.txt         # 의존성 패키지
├── detector/
│   ├── audio_stream.py      # 마이크 오디오 스트림 처리
│   └── yamnet_model.py      # YAMNet 짖음 감지 모듈
└── assets/
    └── responses/           # 짖음 패턴별 텍스트 멘트
```

> 2단계 이후 추가 예정: `tts/`, `avatar/`, `ux/`

---

## 설치 및 실행

### 1. 가상환경 설정

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 실행

```bash
python main.py
```

종료: `Ctrl+C`

---

## 주요 설정 (`config.py`)

| 설정값 | 기본값 | 설명 |
|--------|--------|------|
| `SAMPLE_RATE` | 16000 | YAMNet 요구 샘플레이트 (Hz) |
| `CHUNK_DURATION` | 1.0 | 한 번에 분석할 오디오 길이 (초) |
| `BARK_THRESHOLD` | 0.3 | 짖음 감지 임계값 (높을수록 엄격) |
| `BARK_KEYWORDS` | dog, bark, yip, howl, bow-wow | 짖음 관련 YAMNet 클래스 키워드 |

---

## 개발 단계

| 단계 | 내용 | 상태 |
|------|------|------|
| 1단계 | YAMNet 짖음 감지 + 마이크 연결 | ✅ 진행 중 |
| 2단계 | ElevenLabs TTS API 연동 | 예정 |
| 3단계 | D-ID 얼굴 합성 API 연동 | 예정 |
| 4단계 | 전체 파이프라인 통합 + 디스플레이 출력 | 예정 |
| 5단계 | 테스트 및 최적화 + 발표 준비 | 예정 |

---

## 사용 기술

- **Python 3.x**
- **TensorFlow / TensorFlow Hub** — YAMNet 모델 실행
- **sounddevice** — 실시간 마이크 오디오 스트리밍
- **ElevenLabs API** — 보호자 목소리 클로닝 TTS
- **D-ID API** — 보호자 사진 + 음성 → 말하는 영상 합성
