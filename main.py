import time
from detector.audio_stream import AudioStream
from detector.yamnet_model import BarkDetector

COOLDOWN = 3.0  # 짖음 감지 후 재감지까지 대기 시간 (초)


def main():
    print("=" * 50)
    print("  반려견 짖음 감지 시스템 - Step 1 테스트")
    print("=" * 50)

    detector = BarkDetector()
    stream = AudioStream()

    last_bark_time = 0.0

    try:
        stream.start()
        print("\n[메인] 감지 시작. 종료하려면 Ctrl+C\n")

        while True:
            waveform = stream.read()
            is_bark, score, label = detector.predict(waveform)

            now = time.time()
            if is_bark and (now - last_bark_time) > COOLDOWN:
                last_bark_time = now
                print(f"🐕 짖음 감지! | 클래스: {label} | 점수: {score:.3f}")
            else:
                # 조용할 때는 점수만 출력 (디버깅용)
                top_label = label
                print(f"   대기 중...  | 클래스: {top_label} | 점수: {score:.3f}", end="\r")

    except KeyboardInterrupt:
        print("\n\n[메인] 종료 요청 받음.")
    finally:
        stream.stop()
        print("[메인] 프로그램 종료.")


if __name__ == "__main__":
    main()
