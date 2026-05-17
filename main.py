import sys
import time
import random
import threading
import subprocess
from pathlib import Path
from detector.audio_stream import AudioStream
from detector.yamnet_model import BarkDetector
from assets.responses.responses import RESPONSES

sys.stdout.reconfigure(encoding="utf-8")

COOLDOWN = 5.0
FFPLAY = r"C:\Users\akfrd\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffplay.exe"
VIDEOS_DIR = Path(__file__).parent / "assets" / "videos"


def pick_video() -> tuple[str, str]:
    """사전 생성된 영상 중 하나를 랜덤 선택. (영상경로, 멘트텍스트) 반환"""
    videos = sorted(VIDEOS_DIR.glob("response_*.mp4"))
    if not videos:
        raise FileNotFoundError("사전 생성 영상 없음. 먼저 python prebuild.py 를 실행하세요.")
    idx = random.randrange(len(videos))
    video = videos[idx]
    text = RESPONSES[idx] if idx < len(RESPONSES) else ""
    return str(video), text


def _force_foreground(hwnd: int):
    u32 = __import__("ctypes").windll.user32
    k32 = __import__("ctypes").windll.kernel32
    fg = u32.GetForegroundWindow()
    fg_tid = u32.GetWindowThreadProcessId(fg, None)
    my_tid = k32.GetCurrentThreadId()
    u32.AttachThreadInput(fg_tid, my_tid, True)
    u32.BringWindowToTop(hwnd)
    u32.ShowWindow(hwnd, 3)       # SW_SHOWMAXIMIZED
    u32.SetForegroundWindow(hwnd)
    u32.AttachThreadInput(fg_tid, my_tid, False)


def play_video(path: str):
    title = "DogCare"
    proc = subprocess.Popen(
        [FFPLAY, "-autoexit", "-fs", "-window_title", title, "-loglevel", "quiet", path],
    )
    time.sleep(0.8)
    hwnd = __import__("ctypes").windll.user32.FindWindowW(None, title)
    if hwnd:
        _force_foreground(hwnd)
    proc.wait()


def main():
    print("=" * 50)
    print("  반려견 짖음 감지 시스템")
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
                print(f"\n🐕 짖음 감지! | 클래스: {label} | 점수: {score:.3f}")

                video_path, text = pick_video()
                print(f"[멘트] {text}")

                threading.Thread(target=play_video, args=(video_path,), daemon=True).start()

            else:
                print(f"   대기 중...  | 클래스: {label} | 점수: {score:.3f}", end="\r")

    except KeyboardInterrupt:
        print("\n\n[메인] 종료 요청 받음.")
    finally:
        stream.stop()
        print("[메인] 프로그램 종료.")


if __name__ == "__main__":
    main()
