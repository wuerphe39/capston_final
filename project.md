# 졸업작품 기획안
> AI 기반 반려견 짖음 감지 및 보호자 영상 출력 시스템

---

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | AI 기반 반려견 짖음 감지 및 보호자 영상 출력 시스템 |
| **목적** | 강아지가 짖을 때 보호자의 AI 클로닝 얼굴과 목소리로 반응 |
| **핵심 기술** | 짖음 감지 AI + 목소리 클로닝 TTS + AI 얼굴 합성 |
| **구현 방식** | 클라우드 API 활용 (ElevenLabs + D-ID) |
| **타겟 환경** | 라즈베리파이 or 노트북 + 마이크 + 디스플레이 |

---

## 시스템 전체 흐름

```mermaid
flowchart TD
    A([🎙️ 마이크 입력\n주변 소리 실시간 수집])
    B([🐕 짖음 감지 AI\nYAMNet 로컬 실행])
    C{짖음\n감지됨?}
    D([💬 멘트 결정\n짖음 패턴별 텍스트 선택])
    E([🔊 즉시 응답\n효과음 / '잠깐만~' 안내 음성])
    F([🎵 TTS 생성\nElevenLabs API\n보호자 목소리 클로닝])
    G([🖼️ 로딩 표시\n보호자 사진 + 애니메이션])
    H([🎬 얼굴 합성\nD-ID API\n사진 + 음성 → 영상])
    I([📺 최종 출력\n보호자 얼굴 + 목소리 영상 재생])

    A --> B
    B --> C
    C -- 아니오 --> A
    C -- 예 --> D
    D --> E
    D --> F
    E --> G
    F --> H
    G --> H
    H --> I
    I --> A

    style A fill:#4A90D9,color:#fff,stroke:#2c6fad
    style B fill:#4A90D9,color:#fff,stroke:#2c6fad
    style C fill:#F5A623,color:#fff,stroke:#c47d00
    style D fill:#7B68EE,color:#fff,stroke:#5a4dbf
    style E fill:#27AE60,color:#fff,stroke:#1a7a42
    style F fill:#7B68EE,color:#fff,stroke:#5a4dbf
    style G fill:#27AE60,color:#fff,stroke:#1a7a42
    style H fill:#E74C3C,color:#fff,stroke:#b03a2e
    style I fill:#E74C3C,color:#fff,stroke:#b03a2e
```

---

## 6단계 파이프라인 상세

```mermaid
flowchart LR
    subgraph STEP1["① 입력"]
        A1[🎙️ 마이크]
        A2[실시간 오디오 스트림]
        A1 --> A2
    end

    subgraph STEP2["② 감지 (로컬)"]
        B1[Google YAMNet]
        B2[오디오 분류 AI]
        B3{짖음?}
        B1 --> B2 --> B3
    end

    subgraph STEP3["③ 멘트 결정"]
        C1[짖음 패턴 분석]
        C2[출력 텍스트 선택]
        C1 --> C2
    end

    subgraph STEP4["④ TTS 생성 (클라우드)"]
        D1[ElevenLabs API]
        D2[보호자 목소리 클로닝]
        D3[음성 파일 생성]
        D1 --> D2 --> D3
    end

    subgraph STEP5["⑤ 얼굴 합성 (클라우드)"]
        E1[D-ID API]
        E2[보호자 사진 + 음성]
        E3[말하는 영상 생성]
        E1 --> E2 --> E3
    end

    subgraph STEP6["⑥ 출력"]
        F1[📺 디스플레이]
        F2[🔊 스피커]
    end

    STEP1 --> STEP2
    B3 -- YES --> STEP3
    B3 -- NO --> STEP1
    STEP3 --> STEP4
    STEP4 --> STEP5
    STEP5 --> STEP6

    style STEP1 fill:#EBF5FB,stroke:#2E86C1
    style STEP2 fill:#EBF5FB,stroke:#2E86C1
    style STEP3 fill:#F5EEF8,stroke:#7D3C98
    style STEP4 fill:#EAFAF1,stroke:#1E8449
    style STEP5 fill:#FDEDEC,stroke:#C0392B
    style STEP6 fill:#FEF9E7,stroke:#B7950B
```

---

## 딜레이 UX 처리 흐름

> D-ID API 영상 생성에는 약 **2~5초**의 처리 시간이 소요됩니다. 자연스럽게 처리하기 위해 아래 방식을 적용합니다.

```mermaid
sequenceDiagram
    participant 강아지 as 🐕 강아지
    participant 시스템 as 💻 시스템
    participant ElevenLabs as 🎵 ElevenLabs
    participant DID as 🎬 D-ID API
    participant 디스플레이 as 📺 디스플레이

    강아지->>시스템: 짖음 감지됨
    시스템->>디스플레이: ① 즉시 효과음 / '잠깐만~' 재생
    시스템->>디스플레이: ② 보호자 사진 + 로딩 애니메이션 표시
    시스템->>ElevenLabs: 텍스트 → 보호자 목소리 음성 생성 요청
    ElevenLabs-->>시스템: 음성 파일 반환
    시스템->>DID: 보호자 사진 + 음성 → 영상 생성 요청
    Note over DID: 처리 시간 2~5초
    DID-->>시스템: 영상 파일 반환
    시스템->>디스플레이: ③ 보호자 얼굴 + 목소리 영상 전체 재생
```

---

## 사용 기술 및 API

| 구분 | 기술/API | 역할 | 실행 위치 | 비용 |
|------|----------|------|-----------|------|
| 짖음 감지 | Google YAMNet | 오디오 분류 AI 모델 | 로컬 | 무료 |
| 목소리 클로닝 | ElevenLabs API | 보호자 목소리 학습 + TTS 생성 | 클라우드 | 월 10,000자 무료 |
| 얼굴 합성 | D-ID API | 사진 + 음성 → 말하는 영상 생성 | 클라우드 | 20크레딧 무료 |
| 하드웨어 | 라즈베리파이 or 노트북 | 전체 시스템 구동 + 디스플레이 출력 | 온프레미스 | - |

---

## 기술 스택 구성도

```mermaid
block-beta
    columns 3

    block:INPUT:1
        A["🎙️ 마이크\n(오디오 입력)"]
    end

    block:LOCAL:1
        B["💻 로컬 처리\n─────────────\nGoogle YAMNet\n(짖음 감지)\n\nPython 스크립트\n(파이프라인 제어)"]
    end

    block:CLOUD:1
        C["☁️ 클라우드 API\n─────────────\nElevenLabs\n(목소리 클로닝)\n\nD-ID API\n(얼굴 합성 영상)"]
    end

    block:OUTPUT:3
        D["📺 디스플레이 출력"] E["🔊 스피커 출력"]
    end

    A --> B
    B --> C
    C --> D
    C --> E

    style INPUT fill:#D6EAF8,stroke:#2E86C1
    style LOCAL fill:#D5F5E3,stroke:#1E8449
    style CLOUD fill:#FDEBD0,stroke:#E67E22
    style OUTPUT fill:#E8DAEF,stroke:#7D3C98
```

---

## 개발 단계 및 일정

```mermaid
gantt
    title 개발 일정 (총 약 5~6주)
    dateFormat  YYYY-MM-DD
    section 1단계
    YAMNet 짖음 감지 구현 + 마이크 연결 :a1, 2026-04-21, 14d
    section 2단계
    ElevenLabs TTS API 연동               :a2, after a1, 4d
    section 3단계
    D-ID 얼굴 합성 API 연동               :a3, after a2, 4d
    section 4단계
    전체 파이프라인 통합 + 디스플레이 출력 :a4, after a3, 7d
    section 5단계
    테스트 및 최적화 + 발표 준비          :a5, after a4, 10d
```

### 단계별 상세

| 단계 | 내용 | 난이도 | 예상 기간 |
|------|------|--------|-----------|
| 1단계 | YAMNet 짖음 감지 구현 + 마이크 연결 | ★★☆☆☆ | 1~2주 |
| 2단계 | ElevenLabs TTS API 연동 | ★★☆☆☆ | 3~4일 |
| 3단계 | D-ID 얼굴 합성 API 연동 | ★★☆☆☆ | 3~4일 |
| 4단계 | 전체 파이프라인 통합 + 디스플레이 출력 | ★★★☆☆ | 1주 |
| 5단계 | 테스트 및 최적화 + 발표 준비 | ★★★☆☆ | 1~2주 |

---

## 디렉토리 구조 (예정)

```
dog-care/
├── main.py                  # 전체 파이프라인 진입점
├── detector/
│   ├── yamnet_model.py      # YAMNet 짖음 감지 모듈
│   └── audio_stream.py      # 마이크 오디오 스트림 처리
├── tts/
│   └── elevenlabs_tts.py    # ElevenLabs TTS 음성 생성
├── avatar/
│   └── did_avatar.py        # D-ID 얼굴 합성 영상 생성
├── ux/
│   ├── loading_animation.py # 로딩 중 보호자 사진 + 애니메이션
│   └── player.py            # 영상/음성 재생
├── assets/
│   ├── guardian_photo.jpg   # 보호자 사진
│   └── responses/           # 텍스트 멘트 목록
└── config.py                # API 키 및 설정값
```

---

## 졸업작품 어필 포인트

| 포인트 | 설명 |
|--------|------|
| **AI 기술 2종 결합** | 짖음 분류 AI + 목소리/얼굴 클로닝으로 'AI 융합 프로젝트'로 어필 가능 |
| **실용성** | 반려동물 인구 1,500만 시대에 직접적으로 적용 가능한 아이디어 |
| **실시간 동작** | 단순 영상 재생이 아닌 실시간 AI 생성으로 기술적 완성도 강조 |
| **확장 가능성** | 짖음 패턴 분류, 앱 알림 연동, 다중 반려동물 지원 등으로 발전 가능 |

---

## 확장 아이디어

```mermaid
mindmap
  root((반려견 AI 시스템))
    짖음 분류
      단순 짖음
      공격적 짖음
      분리불안 짖음
      낯선 사람 감지
    알림 연동
      모바일 앱 푸시
      카카오톡 알림
      이메일 리포트
    다중 반려동물
      개체별 인식
      개별 멘트 설정
    보호자 커스터마이징
      멘트 직접 녹음
      반응 강도 조절
      시간대별 설정
```

---

> 본 기획안은 대화 내용을 바탕으로 정리된 초안입니다.
