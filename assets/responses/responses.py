import random

RESPONSES = [
    "괜찮아, 나 여기 있어. 조금만 기다려.",
    "착하지, 착해. 금방 올게.",
    "왜 그래? 걱정 마, 괜찮아.",
    "혼자 있어도 돼, 금방 돌아올게.",
    "짖지 마, 조용히 해. 잘하고 있어.",
    "우리 강아지 최고야. 조금만 참아.",
    "나 금방 와, 기다려.",
]


def get_response() -> str:
    return random.choice(RESPONSES)
