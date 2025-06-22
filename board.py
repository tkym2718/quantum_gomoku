import pyxel
import copy
from typing import Optional

from config import (
    BOARD_SIZE, GRID_SIZE, BOARD_OFFSET, WINNING_LENGTH,
    PLAYER_BLACK, PLAYER_WHITE, OBSERVED_BLACK, OBSERVED_WHITE,
    LABEL_X_OFFSET, LABEL_Y_OFFSET, LABEL_FONT_COLOR, LABELS_X, LABELS_Y,
    STONE_ID_BLACK_90, STONE_ID_BLACK_10   # ← これを追加
)
from stone import Stone

class Board:
    """
    五目並べの盤面を管理するクラス。
    """
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.observed_board = None

    def place_stone(self, row: int, col: int, stone_id: int):
        """
        盤面の指定した位置に石を置きます。

        Args:
            row (int): 石を置く行。
            col (int): 石を置く列。
            stone_id (int): 置く石のID。
        """
        if self.grid[row][col] is None:
            self.grid[row][col] = Stone(stone_id)
            return True
        return False

    def observe_and_check_winner(self, observer_player_type: int) -> Optional[int]:
        """
        盤面全体を観測し、勝利判定を行います。

        Args:
            observer_player_type (int): 観測を実行したプレイヤーのタイプ。

        Returns:
            Optional[int]: 勝者がいればそのプレイヤーのタイプを返す。いなければNone。
        """
        # 1. 盤面を観測して、色を確定させた新しい盤面を作成
        observed_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                stone = self.grid[r][c]
                if stone:
                    observed_board[r][c] = stone.observe()
        self.observed_board = observed_board

        # 2. 勝利判定
        black_wins = self._check_win_for_color(observed_board, OBSERVED_BLACK)
        white_wins = self._check_win_for_color(observed_board, OBSERVED_WHITE)

        # 3. 結果の判定
        if black_wins and white_wins:
            # 両者同時に揃った場合は観測した側の勝ち
            return observer_player_type
        elif black_wins:
            return PLAYER_BLACK
        elif white_wins:
            return PLAYER_WHITE
        else:
            # 勝敗が決まらなければ、観測は失敗
            return None

    def _check_win_for_color(self, board: list[list[int]], color: int) -> bool:
        """指定された色の勝利条件が満たされているかを確認します。"""
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == color:
                    if self._count_in_line(board, r, c, color) >= WINNING_LENGTH:
                        return True
        return False

    def _count_in_line(self, board: list[list[int]], row: int, col: int, color: int) -> int:
        """一列に並んだ指定された色の石の最大数をカウントします。"""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        max_count = 0

        for dr, dc in directions:
            count = 1
            # 正方向
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == color:
                count += 1
                r, c = r + dr, c + dc

            # 逆方向 (元の位置から数え直すので、重複カウントしない)
            r, c = row - dr, col - dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == color:
                count += 1
                r, c = r - dr, c - dc

            if count > max_count:
                max_count = count

        return max_count

    def draw(self):
        """
        盤面と石を描画します。
        """
        # 添え字（x方向: A~O, y方向: 1~15）を描画
        for i in range(BOARD_SIZE):
            # x方向ラベル（A~O）
            x = BOARD_OFFSET + i * GRID_SIZE
            y = BOARD_OFFSET - LABEL_X_OFFSET
            pyxel.text(x + GRID_SIZE // 2 - 2, y, LABELS_X[i], LABEL_FONT_COLOR)
            # y方向ラベル（1~15）
            x2 = BOARD_OFFSET - LABEL_Y_OFFSET
            y2 = BOARD_OFFSET + i * GRID_SIZE
            pyxel.text(x2, y2 + GRID_SIZE // 2 - 2, LABELS_Y[i], LABEL_FONT_COLOR)

        # 盤面の線を描画
        for i in range(BOARD_SIZE):
            # 横線
            pyxel.line(
                BOARD_OFFSET, BOARD_OFFSET + i * GRID_SIZE,
                BOARD_OFFSET + (BOARD_SIZE - 1) * GRID_SIZE, BOARD_OFFSET + i * GRID_SIZE,
                0
            )
            # 縦線
            pyxel.line(
                BOARD_OFFSET + i * GRID_SIZE, BOARD_OFFSET,
                BOARD_OFFSET + i * GRID_SIZE, BOARD_OFFSET + (BOARD_SIZE - 1) * GRID_SIZE,
                0
            )

        # 石を描画
        board_to_draw = self.observed_board if self.observed_board is not None else self.grid

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell = board_to_draw[r][c]
                if cell:
                    x = BOARD_OFFSET + c * GRID_SIZE
                    y = BOARD_OFFSET + r * GRID_SIZE
                    # 観測後盤面なら色番号で描画
                    if self.observed_board is not None:
                        color = 1 if cell == OBSERVED_BLACK else 4  # 黒/白
                        pyxel.circ(x, y, GRID_SIZE // 2 - 1, color)
                    else:
                        pyxel.circ(x, y, GRID_SIZE // 2 - 1, cell.id)

    def save_grid(self):
        """現在の盤面を保存"""
        self._saved_grid = copy.deepcopy(self.grid)

    def restore_grid(self):
        """保存した盤面に戻す"""
        if hasattr(self, "_saved_grid"):
            self.grid = copy.deepcopy(self._saved_grid)
        self.observed_board = None

    def observe_and_visualize(self):
        """観測して盤面を可視化"""
        import random
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                stone = self.grid[r][c]
                if stone:
                    is_black = random.random() < stone.prob_black
                    self.grid[r][c] = Stone(STONE_ID_BLACK_90 if is_black else STONE_ID_BLACK_10)