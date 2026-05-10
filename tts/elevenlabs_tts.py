import requests
from pathlib import Path

API_KEY = "sk_8c447a39e37d7ee9ac0bc1d0b595194a5472c7338a820e46"
VOICE_ID = "p12w67WNfBGpMxeqhQHe"
OUTPUT_PATH = str(Path(__file__).parent.parent / "assets" / "response.mp3")

TTS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
HEADERS = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json",
}


class ElevenLabsSpeaker:
    def speak(self, text: str, output_path: str = OUTPUT_PATH) -> str:
        print(f"[TTS] ElevenLabs 음성 생성 중: {text[:30]}...")
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
            },
            "speed": 0.75,
        }
        resp = requests.post(TTS_URL, headers=HEADERS, json=payload)
        resp.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(resp.content)
        print(f"[TTS] 음성 저장 완료: {output_path}")
        return output_path
