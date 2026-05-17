"""
응답 영상 사전 생성 스크립트
7개 멘트를 미리 TTS + D-ID로 생성해 assets/videos/ 에 저장합니다.
이후 main.py / app.py 는 API 호출 없이 로컬 파일을 바로 재생합니다.
"""
import sys
import time
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path
from assets.responses.responses import RESPONSES
from tts.elevenlabs_tts import ElevenLabsSpeaker
from avatar.did_avatar import DIDAvatar

VIDEOS_DIR = Path(__file__).parent / "assets" / "videos"
VIDEOS_DIR.mkdir(exist_ok=True)


def main():
    print("=" * 54)
    print("  응답 영상 사전 생성")
    print(f"  총 {len(RESPONSES)}개 멘트")
    print("=" * 54)

    tts = ElevenLabsSpeaker()
    avatar = DIDAvatar()

    for i, text in enumerate(RESPONSES, 1):
        video_path = VIDEOS_DIR / f"response_{i:02d}.mp4"

        if video_path.exists():
            print(f"\n[{i}/{len(RESPONSES)}] 이미 존재 — 건너뜀: {video_path.name}")
            continue

        print(f"\n[{i}/{len(RESPONSES)}] {text}")

        tmp_audio = str(Path(__file__).parent / "assets" / f"prebuild_tmp_{i}.mp3")
        audio_path = tts.speak(text, output_path=tmp_audio)
        video_path_str = avatar.generate(audio_path, output_path=str(video_path))

        Path(tmp_audio).unlink(missing_ok=True)
        print(f"  저장 완료: {video_path.name}")

        if i < len(RESPONSES):
            time.sleep(1)

    print("\n" + "=" * 54)
    print("  모든 영상 생성 완료!")
    print(f"  저장 위치: {VIDEOS_DIR}")
    print("=" * 54)


if __name__ == "__main__":
    main()
