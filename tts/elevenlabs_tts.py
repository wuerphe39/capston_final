import requests
from pathlib import Path

API_KEY = "sk_8c447a39e37d7ee9ac0bc1d0b595194a5472c7338a820e46"
DEFAULT_VOICE_ID = "p12w67WNfBGpMxeqhQHe"
OUTPUT_PATH = str(Path(__file__).parent.parent / "assets" / "response.mp3")


class ElevenLabsSpeaker:
    def __init__(self, voice_id: str = DEFAULT_VOICE_ID):
        self._voice_id = voice_id

    def update_voice(self, voice_id: str):
        self._voice_id = voice_id

    def speak(self, text: str, output_path: str = OUTPUT_PATH) -> str:
        print(f"[TTS] ElevenLabs 음성 생성 중: {text[:30]}...")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self._voice_id}"
        headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
            },
            "speed": 0.75,
        }
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(resp.content)
        print(f"[TTS] 음성 저장 완료: {output_path}")
        return output_path
