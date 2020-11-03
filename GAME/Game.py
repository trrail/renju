from GAME import Player
from GAME import Bot
from GAME import Map
from GAME import Const


class Game():
    def __init__(self, is_bot):
        self.players = [Player.Player((0, 0, 0)),
                        Bot.Bot((255, 255, 255)) if is_bot else Player.Player((255, 255, 255))]
        self.map = Map.Map()
        self.is_bot = is_bot
        self.chips_count = 0
        self.current_player = 0

    def make_move(self, mouse_position):
        position = self.define_position(mouse_position)
        if not self.map.map[position[0]][position[1]]:
            self.map.put_chip(self.players[self.current_player].color, position)
            if self.check_winner(position, self.players[self.current_player].color) is not None:
                return self.players[self.current_player].color
            self.current_player = (self.current_player + 1) % len(self.players)
            self.chips_count += 1
            if self.is_bot:
                if self.chips_count == 224:
                    return None
                bot_move_pos = self.players[self.current_player].make_move()
                while self.map.map[bot_move_pos[0]][bot_move_pos[1]] is not None:
                    bot_move_pos = self.players[self.current_player].make_move()
                self.map.put_chip(self.players[self.current_player].color, bot_move_pos)
                if self.check_winner(bot_move_pos, self.players[self.current_player].color):
                    return self.players[self.current_player].color
                self.chips_count += 1
                self.current_player = 0
        return None

    def define_position(self, mouse_pos):
        # При нажатии мыши определяет текущее положение на игровой карте
        x_whole = (mouse_pos[0] - 9) // 25 - 1
        x_residue = (mouse_pos[0] - 9) % 25
        y_whole = (mouse_pos[1] - 9) // 25 - 1
        y_residue = (mouse_pos[1] - 9) % 25
        x_pos = x_whole if x_residue < 12 else x_whole + 1
        y_pos = y_whole if y_residue < 12 else y_whole + 1
        return x_pos, y_pos

    def check_winner(self, pos, color):
        for direction in Const.directions:
            length = self.map.check_winner(pos[0], pos[1], direction, color, 1)
            if length >= 5:
                return color