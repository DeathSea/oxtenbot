from ten import ten,TEN_PLAYER_1,TEN_PLAYER_2,TEN_ALL_FILL,TEN_INV_MOVE,TEN_KEEP_GOING,TEN_PLAYER1_WIN,TEN_PLAYER2_WIN,TEN_INV_PLAYER

from typing import List

class tg_ten(ten):
    def __init__(self):
        super().__init__()
        self._player1_id = 0
        self._player2_id = 0
        self.state = 0

        self._location = [-1, -1]

    @property
    def player1_id(self):
        return self._player1_id

    @player1_id.setter
    def player1_id(self, player1_id : int):
        self._player1_id = player1_id

    @property
    def player2_id(self):
        return self._player2_id

    @player2_id.setter
    def player2_id(self, player2_id : int):
        self._player2_id = player2_id
    
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location: List[int]):
        self._location = location

    def clear_location(self):
        self._location = [-1, -1]

    def set_cur_move(self, cur_player : int, move : List[int]):
        return self.play(TEN_PLAYER_1 if cur_player == self._player1_id else TEN_PLAYER_2, self._location, move)

    def get_tg_tag(self, player):
        t = "⬜️"
        if player == TEN_PLAYER_1:
            t = "❌"
        elif player == TEN_PLAYER_2:
            t = "⭕️"
        return t

    def tg_global_state(self)->str:
        result = []
        for row in super().global_state:
            for column in row:
                t = self.get_tg_tag(column)
                result.append(t)
            result.append("\n")
        return "".join(result)

    def tg_all_state(self) -> str:
        result = []
        for R in super().all_state:
            for r in range(0, 3):
                result.append(self.get_tg_tag(R[0][r][0]))
                result.append(self.get_tg_tag(R[0][r][1]))
                result.append(self.get_tg_tag(R[0][r][2]))
                result.append("|")

                result.append(self.get_tg_tag(R[1][r][0]))
                result.append(self.get_tg_tag(R[1][r][1]))
                result.append(self.get_tg_tag(R[1][r][2]))
                result.append("|")

                result.append(self.get_tg_tag(R[2][r][0]))
                result.append(self.get_tg_tag(R[2][r][1]))
                result.append(self.get_tg_tag(R[2][r][2]))
                result.append("\n")
            result.append("===============\n")
        return "".join(result)

    @property
    def cur_player(self):
        ten_player = super().cur_player
        if ten_player == TEN_PLAYER_1:
            return self.player1_id
        return self.player2_id