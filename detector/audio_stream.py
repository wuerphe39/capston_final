import queue
import numpy as np
import sounddevice as sd
from config import SAMPLE_RATE, CHUNK_DURATION, CHANNELS


class AudioStream:
    def __init__(self):
        self._queue = queue.Queue()
        self._chunk_size = int(SAMPLE_RATE * CHUNK_DURATION)
        self._stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            print(f"[AudioStream] 경고: {status}")
        # 모노로 변환 후 float32 1D 배열로 큐에 추가
        audio = indata[:, 0].astype(np.float32)
        self._queue.put(audio)

    def start(self):
        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            blocksize=self._chunk_size,
            callback=self._callback,
        )
        self._stream.start()
        print(f"[AudioStream] 마이크 스트림 시작 ({SAMPLE_RATE}Hz, {CHUNK_DURATION}초 단위)")

    def read(self):
        """다음 오디오 청크를 반환. 준비될 때까지 블로킹."""
        return self._queue.get()

    def stop(self):
        if self._stream:
            self._stream.stop()
            self._stream.close()
        print("[AudioStream] 스트림 종료")
