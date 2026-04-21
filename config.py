SAMPLE_RATE = 16000        # YAMNet 요구 샘플레이트 (Hz)
CHUNK_DURATION = 1.0       # 한 번에 분석할 오디오 길이 (초)
BARK_THRESHOLD = 0.3       # 짖음 감지 임계값 (0.0 ~ 1.0), 높을수록 엄격
CHANNELS = 1               # 모노

# YAMNet에서 개 짖음 관련 클래스 이름 (부분 일치 검색)
BARK_KEYWORDS = ["dog", "bark", "yip", "howl", "bow-wow"]
