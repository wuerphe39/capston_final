"""
최종 발표용 데모 스크립트
미리 생성된 TTS 음성 + D-ID 영상을 사용해 전체 파이프라인을 시연합니다.
"""
import sys
import time
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AUDIO_PATH = str(Path(__file__).parent / "assets" / "response.mp3")
VIDEO_PATH = str(Path(__file__).parent / "assets" / "response_video.mp4")
GUARDIAN_PHOTO = str(Path(__file__).parent / "assets" / "guardian_photo.jpg")
FFPLAY = r"C:\Users\akfrd\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffplay.exe"


def banner(title: str):
    print(f"\n{'='*54}")
    print(f"  {title}")
    print(f"{'='*54}")
    time.sleep(0.8)


def simulate_bark_detection():
    banner("STEP 1 | 마이크 실시간 감지 (YAMNet)")
    samples = [
        ("Silence",  "0.012"),
        ("Speech",   "0.043"),
        ("Animal",   "0.127"),
        ("Dog bark", "0.821"),
    ]
    for label, score in samples[:-1]:
        print(f"   대기 중...  | 클래스: {label:<12} | 점수: {score}", end="\r")
        time.sleep(1.2)
    print()
    label, score = samples[-1]
    print(f"\n[짖음 감지] 클래스: {label:<12} | 점수: {score}")
    print("[멘트]     괜찮아, 나 여기 있어. 조금만 기다려.")
    time.sleep(1)


def simulate_tts():
    banner("STEP 2 | ElevenLabs 목소리 클로닝 TTS 생성")
    print("[TTS] 보호자 목소리로 음성 생성 중...")
    for i in range(1, 6):
        bar = "█" * i + "░" * (5 - i)
        print(f"      {bar}  {i*20}%", end="\r")
        time.sleep(0.4)
    print(f"\n[TTS] 음성 저장 완료: assets/response.mp3")
    time.sleep(0.5)

    print("\n[재생] 생성된 음성 미리 듣기")
    subprocess.run([FFPLAY, "-autoexit", "-loglevel", "quiet", AUDIO_PATH], check=False)
    time.sleep(0.5)


def simulate_did():
    banner("STEP 3 | D-ID 얼굴 합성 영상 생성")
    print("[D-ID] 보호자 사진 + 음성 업로드 중...")
    time.sleep(0.8)

    print("[D-ID] 영상 생성 요청 완료 — 처리 중 보호자 사진 표시")
    photo_proc = subprocess.Popen(
        [FFPLAY, "-loop", "0", "-loglevel", "quiet", GUARDIAN_PHOTO],
    )

    statuses = ["created", "started", "done"]
    for s in statuses:
        print(f"[D-ID] 상태: {s} ... 대기 중")
        time.sleep(1.5)

    photo_proc.terminate()
    print("[D-ID] 영상 다운로드 완료: assets/response_video.mp4")
    time.sleep(0.5)


def play_video():
    banner("STEP 4 | 보호자 얼굴 + 목소리 영상 재생")
    print("[재생] 디스플레이에 영상 출력 중...\n")
    subprocess.run(
        [FFPLAY, "-autoexit", "-loglevel", "quiet", VIDEO_PATH],
        check=False,
    )


def main():
    print("\n" + "=" * 54)
    print("   AI 기반 반려견 짖음 감지 시스템 — 최종 발표 데모")
    print("=" * 54)
    time.sleep(1.2)

    simulate_bark_detection()
    simulate_tts()
    simulate_did()
    play_video()

    print("\n[완료] 전체 파이프라인 시연 완료.")


if __name__ == "__main__":
    main()
