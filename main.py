import time
import threading
import subprocess
from detector.audio_stream import AudioStream
from detector.yamnet_model import BarkDetector
from tts.xtts_tts import XTTSSpeaker
from avatar.did_avatar import DIDAvatar
from assets.responses.responses import get_response

COOLDOWN = 5.0


def play_audio(path: str):
    import sounddevice as sd
    import soundfile as sf
    data, samplerate = sf.read(path)
    sd.play(data, samplerate)
    sd.wait()


def play_video(path: str):
    """ffplay로 영상 재생 (소리 포함)"""
    subprocess.run(
        ["ffplay", "-autoexit", "-loglevel", "quiet", path],
        check=False,
    )


def main():
    print("=" * 50)
    print("  반려견 짖음 감지 시스템 - Step 3 (D-ID 연동)")
    print("=" * 50)

    detector = BarkDetector()
    stream = AudioStream()
    tts = XTTSSpeaker()
    avatar = DIDAvatar()

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
                print(f"\n🐕 짖음 감지! | 클래스: {label} | 점수: {score:.3f}")

                text = get_response()
                print(f"[멘트] {text}")

                def tts_avatar_and_play():
                    audio_path = tts.speak(text)
                    video_path = avatar.generate(audio_path)
                    play_video(video_path)

                threading.Thread(target=tts_avatar_and_play, daemon=True).start()

            else:
                print(f"   대기 중...  | 클래스: {label} | 점수: {score:.3f}", end="\r")

    except KeyboardInterrupt:
        print("\n\n[메인] 종료 요청 받음.")
    finally:
        stream.stop()
        print("[메인] 프로그램 종료.")


if __name__ == "__main__":
    main()
