"""
중간 발표용 데모 스크립트
미리 생성된 TTS 음성 + D-ID 영상을 사용해 전체 파이프라인을 시연합니다.
"""
import sys
import time
import subprocess
import sounddevice as sd
import soundfile as sf

sys.stdout.reconfigure(encoding="utf-8")

AUDIO_PATH = "assets/response.mp3"
VIDEO_PATH = "assets/response_video.mp4"
FFPLAY = r"C:\Users\akfrd\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffplay.exe"


def step(msg: str):
    print(f"\n{'='*50}")
    print(f"  {msg}")
    print(f"{'='*50}")
    time.sleep(1)


def simulate_bark_detection():
    step("STEP 1 | 마이크 감지 시작")
    print("\n   대기 중...  | 클래스: Silence       | 점수: 0.012", end="\r")
    time.sleep(1.5)
    print("   대기 중...  | 클래스: Speech        | 점수: 0.043", end="\r")
    time.sleep(1.5)
    print("   대기 중...  | 클래스: Animal        | 점수: 0.089", end="\r")
    time.sleep(1.5)
    print("\n")
    print("🐕 짖음 감지! | 클래스: Dog            | 점수: 0.821")
    print("[멘트] 괜찮아, 나 여기 있어. 조금만 기다려.")
    time.sleep(1)


def simulate_tts():
    step("STEP 2 | ElevenLabs 목소리 클로닝 음성 생성")
    print("[TTS] 보호자 목소리로 음성 생성 중...")
    for i in range(1, 6):
        print(f"      생성 진행 중... {'█' * i}{'░' * (5-i)} {i*20}%", end="\r")
        time.sleep(0.4)
    print("\n[TTS] 음성 저장 완료: assets/response.mp3")
    time.sleep(0.5)

    print("\n▶ 생성된 음성 재생:")
    import subprocess
    subprocess.run([FFPLAY, "-autoexit", "-loglevel", "quiet", AUDIO_PATH], check=False)
    time.sleep(0.5)


def simulate_did():
    step("STEP 3 | D-ID 얼굴 합성 영상 생성")
    print("[D-ID] 보호자 사진 + 음성 → 영상 생성 요청...")
    time.sleep(0.8)
    print("[D-ID] 상태: created ... 대기 중")
    time.sleep(1)
    print("[D-ID] 상태: started ... 대기 중")
    time.sleep(1)
    print("[D-ID] 영상 다운로드 완료: assets/response_video.mp4")
    time.sleep(0.5)


def play_video():
    step("STEP 4 | 보호자 얼굴 + 목소리 영상 재생")
    print("📺 영상 재생 중...\n")
    subprocess.run(
        [FFPLAY, "-autoexit", "-loglevel", "quiet", VIDEO_PATH],
        check=False,
    )


def main():
    print("\n" + "="*50)
    print("  반려견 짖음 감지 시스템 - 발표 데모")
    print("="*50)
    time.sleep(1)

    simulate_bark_detection()
    simulate_tts()
    simulate_did()
    play_video()

    print("\n[데모 종료] 전체 파이프라인 시연 완료.")


if __name__ == "__main__":
    main()
