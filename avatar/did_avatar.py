import requests
import time
import subprocess
import tempfile
import os
from pathlib import Path

DID_API_KEY = "YWtmcmRtc2Fsc2d1QGdtYWlsLmNvbQ:ia1IfIMzXyRLilTtQ22vb"
DID_API_URL = "https://api.d-id.com"
GUARDIAN_PHOTO = str(Path(__file__).parent.parent / "assets" / "guardian_photo.jpg")
FFMPEG = r"C:\Users\akfrd\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
OUTPUT_VIDEO = str(Path(__file__).parent.parent / "assets" / "response_video.mp4")

HEADERS = {
    "Authorization": f"Basic {DID_API_KEY}",
    "Content-Type": "application/json",
}


def _wav_to_mp3(wav_path: str) -> str:
    """ffmpeg으로 WAV → MP3 변환, 임시 파일 경로 반환"""
    mp3_path = wav_path.replace(".wav", "_tmp.mp3")
    subprocess.run(
        [FFMPEG, "-y", "-i", wav_path, "-q:a", "2", mp3_path],
        check=True,
        capture_output=True,
    )
    return mp3_path


def _resize_image(max_size: int = 512) -> bytes:
    """D-ID 업로드용으로 이미지를 리사이즈해 bytes 반환"""
    from PIL import Image
    import io
    img = Image.open(GUARDIAN_PHOTO)
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def _upload_image() -> str:
    """보호자 사진을 D-ID에 업로드하고 URL 반환"""
    img_bytes = _resize_image()
    resp = requests.post(
        f"{DID_API_URL}/images",
        headers={"Authorization": f"Basic {DID_API_KEY}"},
        files={"image": ("guardian_photo.jpg", img_bytes, "image/jpeg")},
    )
    resp.raise_for_status()
    url = resp.json().get("url")
    print(f"[D-ID] 사진 업로드 완료: {url}")
    return url


def _upload_audio(mp3_path: str) -> str:
    """MP3 오디오를 D-ID에 업로드하고 URL 반환"""
    with open(mp3_path, "rb") as f:
        resp = requests.post(
            f"{DID_API_URL}/audios",
            headers={"Authorization": f"Basic {DID_API_KEY}"},
            files={"audio": (os.path.basename(mp3_path), f, "audio/mpeg")},
        )
    resp.raise_for_status()
    url = resp.json().get("url")
    print(f"[D-ID] 오디오 업로드 완료: {url}")
    return url


def _create_talk(image_url: str, audio_url: str) -> str:
    """D-ID Talk 영상 생성 요청 후 talk_id 반환"""
    payload = {
        "source_url": image_url,
        "script": {
            "type": "audio",
            "audio_url": audio_url,
        },
        "config": {"stitch": True},
    }
    resp = requests.post(f"{DID_API_URL}/talks", headers=HEADERS, json=payload)
    resp.raise_for_status()
    talk_id = resp.json()["id"]
    print(f"[D-ID] 영상 생성 요청 완료: {talk_id}")
    return talk_id


def _wait_and_download(talk_id: str, output_path: str, timeout: int = 120) -> str:
    """영상 생성 완료 대기 후 다운로드"""
    print("[D-ID] 영상 생성 중...")
    deadline = time.time() + timeout

    while time.time() < deadline:
        resp = requests.get(f"{DID_API_URL}/talks/{talk_id}", headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status")

        if status == "done":
            video_url = data["result_url"]
            video_resp = requests.get(video_url)
            with open(output_path, "wb") as f:
                f.write(video_resp.content)
            print(f"[D-ID] 영상 다운로드 완료: {output_path}")
            return output_path

        if status == "error":
            raise RuntimeError(f"D-ID 영상 생성 실패: {data}")

        print(f"[D-ID] 상태: {status} ... 대기 중")
        time.sleep(3)

    raise TimeoutError("D-ID 영상 생성 시간 초과")


class DIDAvatar:
    def __init__(self):
        print("[D-ID] 초기화 중... 보호자 사진 업로드")
        self._image_url = _upload_image()

    def generate(self, audio_path: str, output_path: str = OUTPUT_VIDEO) -> str:
        mp3_path = _wav_to_mp3(audio_path)
        try:
            audio_url = _upload_audio(mp3_path)
            talk_id = _create_talk(self._image_url, audio_url)
            return _wait_and_download(talk_id, output_path)
        finally:
            if os.path.exists(mp3_path):
                os.remove(mp3_path)
