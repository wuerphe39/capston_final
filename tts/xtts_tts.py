import os
from pathlib import Path

VOICE_SAMPLE = str(Path(__file__).parent.parent / "assets" / "voice_sample_short.wav")
OUTPUT_PATH = str(Path(__file__).parent.parent / "assets" / "response.wav")
VOICE_SAMPLE_TEXT = "괜찮아, 나 여기 있어."


def _patch_torchaudio():
    """torchcodec DLL 문제를 우회해 soundfile로 오디오 로드"""
    import soundfile as sf
    import torch
    import torchaudio

    def sf_load(path, *_):
        data, sr = sf.read(str(path), always_2d=True)
        return torch.tensor(data.T, dtype=torch.float32), sr

    torchaudio.load = sf_load


class XTTSSpeaker:
    def __init__(self):
        if not os.path.exists(VOICE_SAMPLE):
            raise FileNotFoundError(
                f"목소리 샘플 파일이 없습니다: {VOICE_SAMPLE}\n"
                "assets/voice_sample_short.wav 파일을 확인해주세요."
            )
        _patch_torchaudio()
        print("[TTS] F5-TTS 모델 로딩 중... (최초 실행 시 다운로드 발생)")
        from f5_tts.api import F5TTS
        self._tts = F5TTS()
        print("[TTS] 모델 로딩 완료")

    def speak(self, text: str, output_path: str = OUTPUT_PATH) -> str:
        print(f"[TTS] 음성 생성 중: {text[:30]}...")
        self._tts.infer(
            ref_file=VOICE_SAMPLE,
            ref_text=VOICE_SAMPLE_TEXT,
            gen_text=text,
            file_wave=output_path,
        )
        print(f"[TTS] 음성 저장 완료: {output_path}")
        return output_path
