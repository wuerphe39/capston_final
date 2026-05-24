import sys
import time
import json
import random
import threading
from pathlib import Path

from flask import Flask, request, jsonify, render_template, Response, stream_with_context, send_from_directory

sys.stdout.reconfigure(encoding="utf-8")

# ── 상수 ──────────────────────────────────────────────────────────────────────
ASSETS = Path(__file__).parent / "assets"
VIDEOS_DIR = ASSETS / "videos"
VOICE_SAMPLE = ASSETS / "voice_sample_web.wav"
VOICE_ID_FILE = ASSETS / "voice_id.txt"
COOLDOWN = 5.0
EL_API_KEY = "sk_8c447a39e37d7ee9ac0bc1d0b595194a5472c7338a820e46"

app = Flask(__name__)

# ── 파이프라인 상태 ─────────────────────────────────────────────────────────────
_state = {
    "running": False,
    "initializing": False,
    "label": "—",
    "score": 0.0,
    "bark_count": 0,
    "last_message": "",
    "current_video": "",   # 브라우저가 재생할 영상 파일명
}
_stop_event = threading.Event()
_objects = {}


def get_current_voice_id() -> str:
    if VOICE_ID_FILE.exists():
        return VOICE_ID_FILE.read_text(encoding="utf-8").strip()
    return "p12w67WNfBGpMxeqhQHe"


# ── 짖음 감지 루프 ──────────────────────────────────────────────────────────────
def pick_video() -> tuple[str, str]:
    from assets.responses.responses import RESPONSES
    videos = sorted(VIDEOS_DIR.glob("response_*.mp4"))
    if not videos:
        raise FileNotFoundError("사전 생성 영상 없음. python prebuild.py 를 먼저 실행하세요.")
    idx = random.randrange(len(videos))
    text = RESPONSES[idx] if idx < len(RESPONSES) else ""
    return videos[idx].name, text


def bark_loop():
    detector = _objects["detector"]
    stream = _objects["stream"]
    last_bark = 0.0

    stream.start()
    _state["running"] = True

    try:
        while not _stop_event.is_set():
            waveform = stream.read()
            is_bark, score, label = detector.predict(waveform)
            _state["label"] = label
            _state["score"] = round(float(score), 3)

            now = time.time()
            if is_bark and (now - last_bark) > COOLDOWN:
                last_bark = now
                _state["bark_count"] += 1
                video_name, text = pick_video()
                _state["last_message"] = text
                _state["current_video"] = video_name

                def clear_video(name=video_name):
                    time.sleep(3)
                    if _state["current_video"] == name:
                        _state["current_video"] = ""

                threading.Thread(target=clear_video, daemon=True).start()
    finally:
        stream.stop()
        _state["running"] = False


def initialize_and_run():
    from detector.yamnet_model import BarkDetector
    from detector.audio_stream import AudioStream

    _state["initializing"] = True
    try:
        if "detector" not in _objects:
            _objects["detector"] = BarkDetector()
            _objects["stream"] = AudioStream()
    finally:
        _state["initializing"] = False

    bark_loop()


# ── Flask 라우트 ───────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video/<filename>")
def serve_video(filename):
    return send_from_directory(str(VIDEOS_DIR), filename)


@app.route("/status")
def status_stream():
    def generate():
        while True:
            yield f"data: {json.dumps(_state)}\n\n"
            time.sleep(0.5)

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


@app.route("/upload/photo", methods=["POST"])
def upload_photo():
    f = request.files.get("photo")
    if not f:
        return jsonify({"error": "파일 없음"}), 400
    photo_path = str(ASSETS / "guardian_photo.jpg")
    f.save(photo_path)
    if "avatar" in _objects:
        _objects["avatar"].update_photo(photo_path)
    return jsonify({"ok": True})


@app.route("/upload/voice", methods=["POST"])
def upload_voice():
    import requests as req

    f = request.files.get("voice")
    if not f:
        return jsonify({"error": "파일 없음"}), 400
    f.save(str(VOICE_SAMPLE))

    with open(str(VOICE_SAMPLE), "rb") as audio:
        resp = req.post(
            "https://api.elevenlabs.io/v1/voices/add",
            headers={"xi-api-key": EL_API_KEY},
            data={"name": f"dog-care-{int(time.time())}"},
            files={"files": (VOICE_SAMPLE.name, audio, "audio/wav")},
        )
    if resp.status_code != 200:
        return jsonify({"error": resp.text}), 500

    voice_id = resp.json()["voice_id"]
    VOICE_ID_FILE.write_text(voice_id, encoding="utf-8")

    if "tts" in _objects:
        _objects["tts"].update_voice(voice_id)

    return jsonify({"ok": True, "voice_id": voice_id})


@app.route("/start", methods=["POST"])
def start():
    if _state["running"] or _state["initializing"]:
        return jsonify({"ok": True, "message": "이미 실행 중"})

    _stop_event.clear()
    _state["bark_count"] = 0
    _state["last_message"] = ""
    _state["current_video"] = ""

    threading.Thread(target=initialize_and_run, daemon=True).start()
    return jsonify({"ok": True})


@app.route("/stop", methods=["POST"])
def stop():
    _stop_event.set()
    _state["current_video"] = ""
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=False, port=5000, threaded=True)
