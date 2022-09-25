#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging,os
from typing import List,Tuple
# LOG_FILE = "ten.log"
# logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

player1 = 1
player2 = 2

player1_win = 0x010101
player2_win = 0x020202
all_fill = 0x0f0f0f
inv_move = 0xf0f0f0
keep_going = 0x000000

class ten(object):
    def __init__(self):
        self.global_state = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.all_state = [
            [[[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]]],
            [[[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]]],
            [[[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]]],
        ]
        self.state = keep_going
        self.can_move_to_fill = False

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
            return all_fill

        # 横排检查
        for r in tables:
            r_value = (r[0] << 16) | (r[1] << 8)  | r[2]
            if r_value == player1_win:
                return player1_win
            if r_value == player2_win:
                return player2_win

        # 竖排检查
        for c in range(0, 3):
            c_value = (tables[0][c] << 16) | (tables[1][c] << 8) | tables[2][c]
            if c_value == player2_win:
                return player2_win
            if c_value == player1_win:
                return player1_win
        
        # 自左向右斜
        cos_value = tables[0][0] << 16 | tables[1][1] << 8 | tables[2][2]
        if cos_value == player1_win:
            return player1_win
        if cos_value == player2_win:
            return player2_win
        
        # 自右向左斜
        cos_value = tables[2][0] << 16 | tables[1][1] << 8 | tables[0][2]

        if cos_value == player1_win:
            return player1_win
        if cos_value == player2_win:
            return player2_win
        return keep_going

    def game_state_check(self, local : List[int]):
        t = self.all_state[local[0]][local[1]]
        # 小棋盘是否已被占领
        c = self.check_board_state(t)
        if c != keep_going:
            if c == player2_win:
                c = player2
            elif c == player1_win:
                c = player1
            else:
                c = 0xf # 平手填f
            self.global_state[local[0]][local[1]] = c
        return self.check_board_state(self.global_state)

    def play(self, player : int, local : List[int], move : List[int]):

        if self.global_state[local[0]][local[1]] != 0:
            return ([-1, -1], inv_move)

        if self.all_state[local[0]][local[1]][move[0]][move[1]] != 0:
            return ([-1, -1], inv_move)
        self.all_state[local[0]][local[1]][move[0]][move[1]] = player
        r = self.game_state_check(local)

        # 游戏结束
        if r != keep_going:
            return ([0, 0], r)

        # 给予对手的下一步不可走，对手随意挑选小棋盘走，
        if self.global_state[move[0]][move[1]] != 0:
            return ([-1, -1], 0)

        # 否则必须走对手给予的一步
        return (move, 0)

    def print_all_state(self):
        for R in self.all_state:
            for r in range(0,3):
                print(R[0][r][0], R[0][r][1], R[0][r][2], end=" | ")
                print(R[1][r][0], R[1][r][1], R[1][r][2], end=" | ")
                print(R[2][r][0], R[2][r][1], R[2][r][2])
            print("═════════════════════")

    def print_global_state(self):
        for r in self.global_state:
            for c in r:
                print(c, end = " ")
            print()

    @property
    def set_all_state(self, state : List[List[List[List[int]]]]):
        self.all_state = state
    
    @property
    def get_global_state(self):
        return self.global_state
    
    @property
    def get_all_state(self):
        return self.all_state
    


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
    t.set_all_state(ten_tables)
    t.print_all_state()
    print(t.game_state_check((0,0)))
    t.print_global_state()
    play()
