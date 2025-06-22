import pyxel

# 画面設定
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 288
WINDOW_TITLE = "Quantum Gomoku"

# 盤面設定
BOARD_SIZE = 15
GRID_SIZE = 16
BOARD_OFFSET = 30

# 勝利条件
WINNING_LENGTH = 5

# プレイヤー
PLAYER_BLACK = 1
PLAYER_WHITE = 2

# 石の色と確率の対応
# pyxel.colorsのインデックスと石のIDを兼ねる
STONE_ID_BLACK_90 = 1
STONE_ID_BLACK_70 = 2
STONE_ID_BLACK_30 = 3
STONE_ID_BLACK_10 = 4

# 各IDが黒になる確率
PROBABILITY_MAP = {
    STONE_ID_BLACK_90: 0.9,
    STONE_ID_BLACK_70: 0.7,
    STONE_ID_BLACK_30: 0.3,
    STONE_ID_BLACK_10: 0.1,
}

# 観測後の色（勝利判定用）
OBSERVED_BLACK = 10
OBSERVED_WHITE = 11

# カスタムカラー設定
CUSTOM_COLORS = {
    # 90% 黒
    STONE_ID_BLACK_90: 0x000000,
    # 70% 黒
    STONE_ID_BLACK_70: 0x696969,
    # 30% 黒
    STONE_ID_BLACK_30: 0xc0c0c0,
    # 10% 黒
    STONE_ID_BLACK_10: 0xffffff,
    # 背景色
    9: 0xcd853f,
}

# 盤面添字
LABEL_X_OFFSET = 8    # x方向ラベルのy座標
LABEL_Y_OFFSET = 8    # y方向ラベルのx座標
LABEL_FONT_COLOR = 7  # ラベルの色

LABELS_X = [chr(ord('A') + i) for i in range(BOARD_SIZE)]
LABELS_Y = [str(i + 1) for i in range(BOARD_SIZE)]

# 観測回数
MAX_OBSERVATIONS = 5