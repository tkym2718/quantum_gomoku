import random
from config import PROBABILITY_MAP, OBSERVED_BLACK, OBSERVED_WHITE

class Stone:
    """
    量子的な振る舞いをする石を表すクラス。
    """
    def __init__(self, stone_id: int):
        """
        Args:
            stone_id (int): 石の種類を示すID。
        """
        self.id = stone_id
        self.prob_black = PROBABILITY_MAP.get(stone_id, 0)

    def observe(self) -> int:
        """
        確率に基づいて、石の色を観測（確定）します。

        Returns:
            int: 観測後の色（OBSERVED_BLACK または OBSERVED_WHITE）。
        """
        if random.random() < self.prob_black:
            return OBSERVED_BLACK
        else:
            return OBSERVED_WHITE