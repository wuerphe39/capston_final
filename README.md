# AI 기반 반려견 짖음 감지 및 보호자 영상 출력 시스템

> 강아지가 짖으면 보호자의 AI 클로닝 얼굴과 목소리로 반응하는 졸업작품 프로젝트

---

## 개요

마이크로 강아지 짖음을 실시간 감지하고, 보호자의 목소리(ElevenLabs TTS)와 얼굴(D-ID)을 AI로 합성해 디스플레이에 전체화면 출력합니다.
웹 UI를 통해 보호자 사진과 목소리를 등록하고 시스템을 제어할 수 있습니다.

| 항목 | 내용 |
|------|------|
| 짖음 감지 | Google YAMNet (로컬 실행) |
| 목소리 클로닝 | ElevenLabs API (Instant Voice Clone) |
| 얼굴 합성 | D-ID API |
| 웹 인터페이스 | Flask 기반 대시보드 |
| 실행 환경 | Windows 노트북 + 마이크 + 디스플레이 |

---

## 시스템 흐름

```
🎙️ 마이크 입력
    ↓
🐕 YAMNet 짖음 감지 (로컬, 쿨다운 5초)
    ↓ 짖음 감지 시
📂 사전 생성 영상 중 랜덤 선택
    ↓
📺 ffplay로 전체화면 즉시 재생
```

### 영상 사전 생성 흐름 (prebuild.py)

```
💬 멘트 7개
    ↓
🎵 ElevenLabs TTS — 보호자 목소리 클로닝 음성 생성
    ↓
🎬 D-ID API — 보호자 사진 + 음성 → 말하는 영상 생성
    ↓
💾 assets/videos/ 에 저장
```

---

## 디렉토리 구조

```
dog-care/
├── main.py                        # CLI 진입점 (짖음 감지 → 즉시 재생)
├── app.py                         # Flask 웹 서버
├── prebuild.py                    # 응답 영상 사전 생성 스크립트
├── demo.py                        # 발표용 데모 스크립트
├── config.py                      # YAMNet 설정값
├── requirements.txt               # 의존성 패키지
├── templates/
│   └── index.html                 # 웹 대시보드 UI
├── detector/
│   ├── audio_stream.py            # 마이크 실시간 오디오 스트림
│   └── yamnet_model.py            # YAMNet 짖음 감지 모듈
├── tts/
│   └── elevenlabs_tts.py          # ElevenLabs 목소리 클로닝 TTS
├── avatar/
│   └── did_avatar.py              # D-ID 얼굴 합성 영상 생성
└── assets/
    ├── guardian_photo.jpg          # 보호자 사진 (gitignore)
    ├── voice_sample.wav            # 보호자 목소리 녹음 (gitignore)
    ├── videos/                     # 사전 생성 영상 저장 폴더
    │   ├── response_01.mp4
    │   └── ...
    └── responses/
        └── responses.py           # 짖음 감지 시 출력 멘트 목록 (7개)
```

---

## 설치 및 실행

### 1. 가상환경 설정

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 응답 영상 사전 생성 (최초 1회)

```bash
python prebuild.py
```

7개 멘트 영상을 `assets/videos/`에 저장합니다. 약 2~3분 소요.

### 3. 웹 UI로 실행 (권장)

```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속 후:
- 보호자 사진 업로드 및 등록
- 보호자 목소리 업로드 및 ElevenLabs 클로닝 등록
- **시작** 버튼으로 짖음 감지 시작

### 4. CLI로 실행

```bash
python main.py
```

### 5. 발표용 데모 실행

```bash
python demo.py
```

종료: `Ctrl+C`

---

## 주요 설정

### `config.py` — YAMNet 설정

| 설정값 | 기본값 | 설명 |
|--------|--------|------|
| `SAMPLE_RATE` | 16000 | YAMNet 요구 샘플레이트 (Hz) |
| `CHUNK_DURATION` | 1.0 | 한 번에 분석할 오디오 길이 (초) |
| `BARK_THRESHOLD` | 0.3 | 짖음 감지 임계값 (높을수록 엄격) |
| `BARK_KEYWORDS` | dog, bark, yip, howl, bow-wow | YAMNet 짖음 클래스 키워드 |

### `tts/elevenlabs_tts.py` — TTS 설정

| 설정값 | 값 | 설명 |
|--------|-----|------|
| `model_id` | eleven_multilingual_v2 | 다국어 TTS 모델 |
| `speed` | 0.75 | 음성 속도 (1.0 기본, 낮을수록 느림) |
| `stability` | 0.5 | 음성 안정성 |
| `similarity_boost` | 0.75 | 원본 목소리 유사도 |

---

## 개발 단계 및 현황

| 단계 | 내용 | 상태 |
|------|------|------|
| 1단계 | YAMNet 짖음 감지 + 마이크 연결 | ✅ 완료 |
| 2단계 | ElevenLabs TTS API 연동 | ✅ 완료 |
| 3단계 | D-ID 얼굴 합성 API 연동 | ✅ 완료 |
| 4단계 | 전체 파이프라인 통합 + 디스플레이 출력 | ✅ 완료 |
| 5단계 | 테스트 및 최적화 + 발표 준비 | ✅ 완료 |
| 6단계 | 웹 UI 추가 (사진/목소리 등록, 원격 제어) | ✅ 완료 |

---

## 개발 과정에서 발생한 문제점 및 해결 방안

### 문제 1. Coqui TTS (XTTS v2) Windows 빌드 실패

**상황**
로컬 목소리 클로닝을 위해 Coqui TTS(XTTS v2) 설치를 시도했으나 Windows에서 빌드 실패.

**원인**
- `TTS.tts.utils.monotonic_align.core` C 확장 모듈 컴파일 시 Microsoft Visual C++ 필요
- Visual Studio Build Tools 2026이 설치되어 있었으나 Python 빌드 시스템이 인식 불가

**해결**
- 1차 시도: F5-TTS (C 컴파일 불필요) 로 교체 → 한국어 발음 품질 불안정
- 최종 해결: **ElevenLabs API Creator 플랜**으로 전환 → 한국어 품질 우수, 설치 간단

---

### 문제 2. F5-TTS torchcodec DLL 로드 실패

**상황**
F5-TTS 설치는 성공했으나 실행 시 `Could not load libtorchcodec` 에러 발생.

**원인**
`torchaudio.load`가 내부적으로 `torchcodec`을 사용하는데, Windows에서 FFmpeg DLL을 찾지 못함.

**해결**
`torchaudio.load`를 `soundfile`로 몽키패칭하여 torchcodec 우회:

```python
import soundfile as sf
import torch, torchaudio

def sf_load(path, *_):
    data, sr = sf.read(str(path), always_2d=True)
    return torch.tensor(data.T, dtype=torch.float32), sr

torchaudio.load = sf_load
```

---

### 문제 3. D-ID API 이미지 크기 초과 (InvalidFileSizeError)

**상황**
D-ID `/talks` 엔드포인트 호출 시 `file size exceeded 10 MB` 에러.

**원인**
보호자 사진 원본 해상도가 2544×3392으로 너무 높음.

**해결**
PIL로 업로드 전 512px로 리사이즈:

```python
from PIL import Image
import io

img = Image.open(GUARDIAN_PHOTO)
img.thumbnail((512, 512), Image.LANCZOS)
buf = io.BytesIO()
img.save(buf, format="JPEG", quality=90)
```

---

### 문제 4. D-ID audio_url base64 방식 500 에러

**상황**
음성을 base64로 인코딩해 `data:audio/wav;base64,...` 형식으로 전달했으나 500 에러.

**원인**
D-ID가 data URI 형식의 오디오를 지원하지 않음.

**해결**
음성 파일을 D-ID `/audios` 엔드포인트에 별도 업로드 후 S3 URL을 `audio_url`로 사용.

---

### 문제 5. ElevenLabs API 키 권한 오류 (401 Unauthorized)

**상황**
ElevenLabs API 키 생성 후 TTS 호출 시 `missing_permissions` 에러.

**원인**
API 키 생성 시 **키 제한** 토글이 활성화된 상태로 생성되어 모든 엔드포인트 접근이 차단됨.

**해결**
API 키 편집 → **키 제한 토글 OFF** → 모든 엔드포인트 접근 허용.

---

### 문제 6. ElevenLabs MP3 → D-ID 업로드 시 파일 충돌

**상황**
ElevenLabs가 MP3를 출력하는데, D-ID 모듈이 WAV→MP3 변환을 시도하다 같은 파일을 덮어쓰려 해 에러 발생.

**원인**
`did_avatar.py`의 `_wav_to_mp3` 함수가 `.mp3` 확장자 입력을 처리하지 못함.

**해결**
입력 파일 확장자를 확인해 WAV일 때만 변환, MP3는 바로 업로드:

```python
if audio_path.endswith(".wav"):
    mp3_path = _wav_to_mp3(audio_path)
    remove_after = True
else:
    mp3_path = audio_path
    remove_after = False
```

---

### 문제 7. D-ID 402 Payment Required

**상황**
D-ID `/talks` 호출 시 `402 Payment Required` 에러 발생.

**원인**
무료 플랜 크레딧(20크레딧) 소진. 크레딧은 매달 1일 초기화.

**해결**
D-ID Lite 플랜 구독 (월 400크레딧) 또는 응답 영상을 미리 생성해 로컬 저장 후 재사용.

---

### 문제 8. 응답 지연 (짖음 감지 후 10~15초 대기)

**상황**
짖음 감지 후 TTS 생성 (~2초) + D-ID 영상 생성 (~12초) 로 인해 반응이 너무 느림.

**원인**
매번 짖음 감지 시마다 API를 실시간 호출.

**해결**
`prebuild.py`로 7개 응답 영상을 사전 생성해 `assets/videos/`에 저장.
짖음 감지 시 로컬 파일을 랜덤 선택해 즉시 재생 → 반응 속도 대폭 향상.

---

### 문제 9. 영상이 백그라운드에서 실행됨

**상황**
백그라운드 스레드에서 ffplay를 실행하면 영상 창이 다른 창 뒤로 숨음.

**원인**
Windows는 포그라운드 권한이 없는 프로세스가 `SetForegroundWindow`를 호출하는 것을 차단.

**해결**
`AttachThreadInput`으로 포그라운드 스레드의 입력 권한을 임시 획득 후 강제로 창을 앞으로 이동:

```python
import ctypes

def _force_foreground(hwnd):
    u32 = ctypes.windll.user32
    k32 = ctypes.windll.kernel32
    fg = u32.GetForegroundWindow()
    fg_tid = u32.GetWindowThreadProcessId(fg, None)
    my_tid = k32.GetCurrentThreadId()
    u32.AttachThreadInput(fg_tid, my_tid, True)
    u32.BringWindowToTop(hwnd)
    u32.ShowWindow(hwnd, 3)
    u32.SetForegroundWindow(hwnd)
    u32.AttachThreadInput(fg_tid, my_tid, False)
```

---

## 사용 기술

| 기술 | 역할 |
|------|------|
| Python 3.11 | 전체 시스템 구현 |
| TensorFlow / TensorFlow Hub | YAMNet 짖음 감지 모델 실행 |
| sounddevice | 실시간 마이크 오디오 스트리밍 |
| ElevenLabs API | 보호자 목소리 클로닝 TTS 생성 |
| D-ID API | 보호자 사진 + 음성 → 말하는 영상 합성 |
| Flask | 웹 대시보드 서버 |
| ffmpeg / ffplay | 오디오 변환 및 영상 재생 |
| Pillow | 보호자 사진 리사이즈 전처리 |
| requests / soundfile | HTTP API 통신 및 오디오 파일 처리 |
