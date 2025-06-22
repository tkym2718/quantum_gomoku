import pyxel
import math

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, BOARD_OFFSET, GRID_SIZE,
    BOARD_SIZE, CUSTOM_COLORS, PLAYER_BLACK, PLAYER_WHITE
)
from board import Board
from player import Player

class App:
    """
    ゲーム全体を管理し、実行するクラス。
    """
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=WINDOW_TITLE, fps=60)

        # --- アセットのロード ---
        # assets/sprite.pyxres というファイルを作成してください。
        # このファイルがないとエラーになります。
        try:
            pyxel.load("assets/sprite.pyxres")
        except FileNotFoundError:
            print("警告: assets/sprite.pyxres が見つかりません。")
            # ダミーの画像リソースを作成
            pyxel.image(0).cls(0)


        # --- 色と音楽の初期設定 ---
        for key, value in CUSTOM_COLORS.items():
            pyxel.colors[key] = value
        pyxel.playm(0, loop=True)
        self.is_observing = False
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """
        ゲームの状態を初期化またはリセットします。
        """
        self.game_state = "playing"  # playing, observing, game_over
        self.board = Board()
        self.players = [Player(PLAYER_BLACK), Player(PLAYER_WHITE)]
        self.current_player_index = 0
        self.winner = None
        self.message = ""
        self.message_timer = 0
        self.observer_index = None

    def update(self):
        """
        ゲームの状態をフレームごとに更新します。
        """
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0 and self.game_state == "observing":
                # 観測結果の判定
                if self.observation_result:
                    self.winner = self.observation_result
                    self.game_state = "game_over"
                else:
                    self.message = "WINNER NOT DETERMINED."
                    self.message_timer = 90  # 判定不可メッセージの表示時間
                    self.game_state = "playing" # playing状態に戻し、メッセージだけ表示
            return

        if self.game_state == "playing":
            self.update_playing()
        elif self.game_state == "game_over":
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()

    def update_playing(self):
        """プレイ中の更新処理"""
        current_player = self.players[self.current_player_index]

        # 石を置く処理
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            row, col = self.xy_to_grid(pyxel.mouse_x, pyxel.mouse_y)
            if row is not None:
                stone_id = current_player.get_next_stone_id()
                if self.board.place_stone(row, col, stone_id):
                    current_player.confirm_placement()
                    self.current_player_index = 1 - self.current_player_index

        # 観測処理
        if pyxel.btnp(pyxel.KEY_O):
            if not self.is_observing:
                self.board.save_grid()
                self.is_observing = True
                self.observer_index = self.current_player_index  # 観測者を記録
                self.message = "OBSERVING... (Press O again to restore)"
                self.message_timer = 0

                # 観測後の勝利判定（確定色で判定！）
                observer_player_type = [PLAYER_BLACK, PLAYER_WHITE][self.observer_index]
                winner = self.board.observe_and_check_winner(observer_player_type)
                self.players[self.observer_index].observation_count -= 1

                if winner is not None:
                    self.winner = winner
                    self.game_state = "game_over"
                    self.message = "WINNER DETERMINED BY OBSERVATION!"
                    self.message_timer = 90
                else:
                    # 可視化だけ行う
                    self.board.observe_and_visualize()
            else:
                self.board.restore_grid()
                self.is_observing = False
                self.message = "RESTORED ORIGINAL BOARD"
                self.message_timer = 60

    def draw(self):
        """
        画面を描画します。
        """
        pyxel.cls(9)  # 背景色でクリア
        self.board.draw()
        self._draw_ui()

        # メッセージや結果の表示
        if self.message_timer > 0:
            pyxel.rect(0, SCREEN_HEIGHT // 2 - 20, SCREEN_WIDTH, 40, 0)
            text_x = (SCREEN_WIDTH - len(self.message) * pyxel.FONT_WIDTH) // 2
            pyxel.text(text_x, SCREEN_HEIGHT // 2 - 4, self.message, 7)

        if self.game_state == "game_over":
            if self.winner == PLAYER_BLACK:
                result_text = "PLAYER 1 (BLACK) WINS!"
            else:
                result_text = "PLAYER 2 (WHITE) WINS!"

            pyxel.rect(0, SCREEN_HEIGHT // 2 - 20, SCREEN_WIDTH, 40, 8)
            text_x = (SCREEN_WIDTH - len(result_text) * pyxel.FONT_WIDTH) // 2
            pyxel.text(text_x, SCREEN_HEIGHT // 2 - 10, result_text, 7)

            restart_text = "PRESS 'R' TO RESTART"
            text_x = (SCREEN_WIDTH - len(restart_text) * pyxel.FONT_WIDTH) // 2
            pyxel.text(text_x, SCREEN_HEIGHT // 2 + 6, restart_text, 7)

        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, 16, 32, 16, 16, 9)


    def _draw_ui(self):
        """UI要素を描画します"""
        ui_x = 300
        ui_y = 20

        # 現在のプレイヤー
        turn_player_index = self.current_player_index
        turn_player_obj = self.players[turn_player_index]
        if turn_player_index == 0:
            player_text = "BLACK TURN"
        else:
            player_text = "WHITE TURN"
        pyxel.text(ui_x, ui_y, player_text, 7)

        # 次に置く石
        next_stone_id = turn_player_obj.get_next_stone_id()
        pyxel.text(ui_x, ui_y + 20, "NEXT STONE:", 7)
        pyxel.circ(ui_x + 80, ui_y + 22, 7, next_stone_id)

        # 残り観測回数
        p1_obs = self.players[0].observation_count
        p2_obs = self.players[1].observation_count
        pyxel.text(ui_x, ui_y + 50, f"P1 OBSERVE: {p1_obs}", 7)
        pyxel.text(ui_x, ui_y + 60, f"P2 OBSERVE: {p2_obs}", 7)

        # 操作説明
        pyxel.text(ui_x, ui_y + 90, "L-CLICK: PLACE STONE", 7)
        pyxel.text(ui_x, ui_y + 100, "'O' KEY: OBSERVE", 7)
        if self.game_state == "game_over":
            pyxel.text(ui_x, ui_y + 120, "'R' KEY: RESTART", 7)


    def xy_to_grid(self, x, y):
        """マウス座標を盤面のマス目に変換。範囲外ならNoneを返す"""
        if (BOARD_OFFSET - GRID_SIZE // 2 < x < BOARD_OFFSET + (BOARD_SIZE - 0.5) * GRID_SIZE and
            BOARD_OFFSET - GRID_SIZE // 2 < y < BOARD_OFFSET + (BOARD_SIZE - 0.5) * GRID_SIZE):

            col = round((x - BOARD_OFFSET) / GRID_SIZE)
            row = round((y - BOARD_OFFSET) / GRID_SIZE)
            return row, col
        return None, None


if __name__ == "__main__":
    App()