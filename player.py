from config import (
    PLAYER_BLACK, PLAYER_WHITE,
    STONE_ID_BLACK_90, STONE_ID_BLACK_70,
    STONE_ID_BLACK_30, STONE_ID_BLACK_10,
    MAX_OBSERVATIONS
)

class Player:
    """
    プレイヤーの状態と行動を管理するクラス。
    """
    def __init__(self, player_type: int):
        """
        Args:
            player_type (int): プレイヤーの種類 (PLAYER_BLACK or PLAYER_WHITE).
        """
        self.type = player_type
        self.observation_count = MAX_OBSERVATIONS

        if self.type == PLAYER_BLACK:
            self.stone_ids = [STONE_ID_BLACK_90, STONE_ID_BLACK_70]
        else:
            self.stone_ids = [STONE_ID_BLACK_10, STONE_ID_BLACK_30]

        self.next_stone_index = 0

    def get_next_stone_id(self) -> int:
        """
        次に置く石のIDを取得します。

        Returns:
            int: 次に置くべき石のID。
        """
        return self.stone_ids[self.next_stone_index]

    def confirm_placement(self):
        """
        石を置いたことを確定し、次に使う石を切り替えます。
        """
        self.next_stone_index = 1 - self.next_stone_index

    def can_observe(self) -> bool:
        """
        観測が実行可能かを確認します。

        Returns:
            bool: 観測回数が残っていればTrue。
        """
        return self.observation_count > 0

    def use_observation(self):
        """
        観測回数を1消費します。
        """
        if self.can_observe():
            self.observation_count -= 1