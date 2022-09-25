from ten import ten,player1,player2

from typing import List

class tg_ten(ten):
    def __init__(self):
        super(ten).__init__()
        self.player1_id = 0
        self.player2_id = 0
        self.state = 0

        self.cur_player = 0
        self.cur_location = [0, 0]
    @property
    def set_player1_id(self, player1 : int):
        self.player1_id = player1
    @property
    def set_player2_id(self, player2 : int):
        self.player2_id = player2
    
    def set_cur_player_and_location(self, playerid: int, location: List[int]):
        self.cur_player = player1 if playerid == self.player1_id else player2
        self.cur_location = location

    def set_cur_move(self, move : List[int]):
        return self.play(self.cur_player, self.cur_location, move)
