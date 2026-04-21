import numpy as np
import tensorflow_hub as hub
import csv
import io
import urllib.request
from config import BARK_THRESHOLD, BARK_KEYWORDS

YAMNET_MODEL_URL = "https://tfhub.dev/google/yamnet/1"
YAMNET_CLASS_MAP_URL = (
    "https://raw.githubusercontent.com/tensorflow/models/master"
    "/research/audioset/yamnet/yamnet_class_map.csv"
)


class BarkDetector:
    def __init__(self):
        print("[BarkDetector] YAMNet 모델 로딩 중... (최초 실행 시 다운로드 발생)")
        self._model = hub.load(YAMNET_MODEL_URL)
        self._class_names = self._load_class_names()
        self._bark_indices = self._find_bark_indices()
        print(f"[BarkDetector] 짖음 관련 클래스 {len(self._bark_indices)}개 감지 대상:")
        for idx in self._bark_indices:
            print(f"  [{idx}] {self._class_names[idx]}")

    def _load_class_names(self):
        raw = urllib.request.urlopen(YAMNET_CLASS_MAP_URL).read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(raw))
        return [row["display_name"] for row in reader]

    def _find_bark_indices(self):
        indices = []
        for i, name in enumerate(self._class_names):
            if any(kw in name.lower() for kw in BARK_KEYWORDS):
                indices.append(i)
        return indices

    def predict(self, waveform: np.ndarray) -> tuple[bool, float, str]:
        """
        Returns:
            is_bark  : 짖음 감지 여부
            score    : 최고 관련 클래스 점수 (0.0 ~ 1.0)
            label    : 해당 클래스 이름
        """
        scores, _, _ = self._model(waveform)
        mean_scores = np.mean(scores.numpy(), axis=0)

        bark_scores = {idx: mean_scores[idx] for idx in self._bark_indices}
        best_idx = max(bark_scores, key=bark_scores.get)
        best_score = bark_scores[best_idx]
        best_label = self._class_names[best_idx]

        is_bark = best_score >= BARK_THRESHOLD
        return is_bark, float(best_score), best_label
