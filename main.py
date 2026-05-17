import sys
import time
import threading
import subprocess
from pathlib import Path
from detector.audio_stream import AudioStream
from detector.yamnet_model import BarkDetector
from tts.elevenlabs_tts import ElevenLabsSpeaker
from avatar.did_avatar import DIDAvatar
from assets.responses.responses import get_response

sys.stdout.reconfigure(encoding="utf-8")

COOLDOWN = 5.0
FFPLAY = r"C:\Users\akfrd\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffplay.exe"
GUARDIAN_PHOTO = str(Path(__file__).parent / "assets" / "guardian_photo.jpg")


def show_photo() -> subprocess.Popen:
    """보호자 사진을 창에 띄우고 프로세스 반환 (영상 준비될 때까지 유지)"""
    return subprocess.Popen(
        [FFPLAY, "-loop", "0", "-loglevel", "quiet", GUARDIAN_PHOTO],
    )


def play_video(path: str):
    subprocess.run(
        [FFPLAY, "-autoexit", "-loglevel", "quiet", path],
        check=False,
    )


def main():
    print("=" * 50)
    print("  반려견 짖음 감지 시스템")
    print("=" * 50)

    detector = BarkDetector()
    stream = AudioStream()
    tts = ElevenLabsSpeaker()
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

                def tts_avatar_and_play(t=text):
                    photo_proc = show_photo()
                    try:
                        audio_path = tts.speak(t)
                        video_path = avatar.generate(audio_path)
                    finally:
                        photo_proc.terminate()
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
