#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging,os
from typing import List,Tuple
# LOG_FILE = "ten.log"
# logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

TEN_PLAYER_1 = 1
TEN_PLAYER_2 = 2

TEN_PLAYER1_WIN = 0x010101
TEN_PLAYER2_WIN = 0x020202
TEN_ALL_FILL = 0x0f0f0f
TEN_INV_MOVE = 0xf0f0f0
TEN_KEEP_GOING = 0x000000
TEN_INV_PLAYER = 0x10101010

class ten(object):
    def __init__(self):
        self._global_state = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self._all_state = [
            [[[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]]],
            [[[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]]],
            [[[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]]],
        ]
        self.state = TEN_KEEP_GOING
        self.can_move_to_fill = False
        self._cur_player = 0

    def check_board_state(self, tables: List[List[int]]):
        r_win = None
        a_f = True
        # 检查是不是无路可走了
        for r in tables:
            for c in r:
                if c == 0:
                    a_f = False
                    break
            if not a_f:
                break
        if a_f:
            return TEN_ALL_FILL

        # 横排检查
        for r in tables:
            r_value = (r[0] << 16) | (r[1] << 8)  | r[2]
            if r_value == TEN_PLAYER1_WIN:
                return TEN_PLAYER1_WIN
            if r_value == TEN_PLAYER2_WIN:
                return TEN_PLAYER2_WIN

        # 竖排检查
        for c in range(0, 3):
            c_value = (tables[0][c] << 16) | (tables[1][c] << 8) | tables[2][c]
            if c_value == TEN_PLAYER2_WIN:
                return TEN_PLAYER2_WIN
            if c_value == TEN_PLAYER1_WIN:
                return TEN_PLAYER1_WIN
        
        # 自左向右斜
        cos_value = tables[0][0] << 16 | tables[1][1] << 8 | tables[2][2]
        if cos_value == TEN_PLAYER1_WIN:
            return TEN_PLAYER1_WIN
        if cos_value == TEN_PLAYER2_WIN:
            return TEN_PLAYER2_WIN
        
        # 自右向左斜
        cos_value = tables[2][0] << 16 | tables[1][1] << 8 | tables[0][2]

        if cos_value == TEN_PLAYER1_WIN:
            return TEN_PLAYER1_WIN
        if cos_value == TEN_PLAYER2_WIN:
            return TEN_PLAYER2_WIN
        return TEN_KEEP_GOING

    def game_state_check(self, local : List[int]):
        t = self._all_state[local[0]][local[1]]
        # 小棋盘是否已被占领
        c = self.check_board_state(t)
        if c != TEN_KEEP_GOING:
            if c == TEN_PLAYER2_WIN:
                c = TEN_PLAYER_2
            elif c == TEN_PLAYER1_WIN:
                c = TEN_PLAYER_1
            else:
                c = 0xf # 平手填f
            self._global_state[local[0]][local[1]] = c
        return self.check_board_state(self._global_state)

    def play(self, player : int, local : List[int], move : List[int]):

        if self._global_state[local[0]][local[1]] != 0:
            return ([-1, -1], TEN_INV_MOVE)

        if self._all_state[local[0]][local[1]][move[0]][move[1]] != 0:
            return ([-1, -1], TEN_INV_MOVE)

        if self._cur_player == 0:
            self._cur_player = player
        elif self._cur_player == TEN_PLAYER_1:
            if player == TEN_PLAYER_1:
                return ([-1, -1], TEN_INV_PLAYER)
            self._cur_player = TEN_PLAYER_2
        elif self._cur_player == TEN_PLAYER_2:
            if player == TEN_PLAYER_2:
                return ([-1, -1], TEN_INV_PLAYER)
            self._cur_player = TEN_PLAYER_1

        self._all_state[local[0]][local[1]][move[0]][move[1]] = player
        r = self.game_state_check(local)

        # 游戏结束
        if r != TEN_KEEP_GOING:
            return ([0, 0], r)

        # 给予对手的下一步不可走，对手随意挑选小棋盘走，
        if self._global_state[move[0]][move[1]] != 0:
            return ([-1, -1], 0)

        # 否则必须走对手给予的一步
        return (move, 0)

    def print_all_state(self):
        for R in self._all_state:
            for r in range(0,3):
                print(R[0][r][0], R[0][r][1], R[0][r][2], end=" | ")
                print(R[1][r][0], R[1][r][1], R[1][r][2], end=" | ")
                print(R[2][r][0], R[2][r][1], R[2][r][2])
            print("═════════════════════")

    def print_global_state(self):
        for r in self._global_state:
            for c in r:
                print(c, end = " ")
            print()

    @property
    def all_state(self):
        return self._all_state

    @all_state.setter
    def all_state(self, state : List[List[List[List[int]]]]):
        self._all_state = state
    
    @property
    def global_state(self):
        return self._global_state
    
    @property
    def cur_player(self):
        return self._cur_player


def play():
    next_local = [-1, -1]
    player = 1
    game = ten()
    while 1:
        print("stats game:")
        game.print_all_state()
        print("global status:")
        game.print_global_state()
        if next_local == [-1,-1]:
            next_local[0] = int(input("big checkerboard row(0,1,2):"))
            next_local[1] = int(input("big checkerboard col(0,1,2):"))
        else:
            print("you can only play in", next_local[0], next_local[1],"big checkerboard")
        move = [0,0]
        move[0] = int(input("small checkerboard row(0,1,2):"))
        move[1] = int(input("small checkerboard row(0,1,2):"))
        c = game.play(player, next_local, move)
        if c[1] != 0:
            break
        next_local = c[0]
        player = 2 if player == 1 else 1
    print("stats game:")
    game.print_all_state()
    print("global status:")
    game.print_global_state()
    print("game end")


if __name__ == '__main__':
    t = ten()
    test_tables = [[1,1,1], [0,0,0], [0,0,0]]
    print(hex(t.check_board_state(test_tables)))

    test_tables = [[2,2,2], [0,0,0], [0,0,0]]
    print(hex(t.check_board_state(test_tables)))

    test_tables = [[0,0,0], [1,1,1], [0,0,0]]
    print(hex(t.check_board_state(test_tables)))

    test_tables = [[0,0,0], [2,2,2], [0,0,0]]
    print(hex(t.check_board_state(test_tables)))

    test_tables = [[0,0,0], [0,0,0], [1,1,1]]
    print(hex(t.check_board_state(test_tables)))

    test_tables = [[0,0,0], [0,0,0], [2,2,2]]
    print(hex(t.check_board_state(test_tables)))

    test_tables = [[1,0,0], [0,1,0], [0,0,1]]
    print(hex(t.check_board_state(test_tables)))

    test_tables = [[0,0,1], [0,1,0], [1,0,0]]
    print(hex(t.check_board_state(test_tables)))

    test_tables = [[2,0,0], [0,2,0], [0,0,2]]
    print(hex(t.check_board_state(test_tables)))

    test_tables = [[0,0,2], [0,2,0], [2,0,0]]
    print(hex(t.check_board_state(test_tables)))

    test_tables = [ [1,2,1], [1,2,2], [2,1,2]]
    print(hex(t.check_board_state(test_tables)))

    ten_tables = [
        [
            [
                [1,1,1], 
                [0,2,0], 
                [0,0,1]
            ],           [
                          [0,2,0], 
                          [1,2,0], 
                          [0,2,1]
                          ],        [
                                      [1,0,2], 
                                      [0,1,0], 
                                      [0,0,1]
                                    ]
        ],
        [
            [[1,1,1], [0,0,0], [2,2,0]], [[0,2,0], [0,0,1], [2,0,0]], [[0,0,2], [0,1,0], [1,0,2]]
        ],
        [
            [[1,0,2], [2,0,1], [1,1,0]], [[0,0,2], [1,0,0], [2,2,0]], [[0,1,0], [0,2,0], [2,1,0]]
        ],
    ]
    t.all_state = ten_tables
    t.print_all_state()
    print(t.game_state_check((0,0)))
    t.print_global_state()
    play()
