from GAME import Player
from GAME import Bot
from GAME import Map
from GAME import Const


class Game:
    def __init__(self, is_bot):
        self.players = [Player.Player((0, 0, 0)),
                        Bot.Bot((255, 255, 255)) if is_bot else Player.Player((255, 255, 255))]
        self.map = Map.Map()
        self.is_bot = is_bot
        self.chips_count = 0
        self.current_player = 0

    def take_pos(self):
        return self.players[self.current_player].make_move()

    def make_move(self, position):
        '''
        position = self.define_position(mouse_position)
        if not self.map.map[position[0]][position[1]]:
            self.map.put_chip(self.players[self.current_player].color, position)
            if self.check_winner(position, self.players[self.current_player].color) is not None:
                return self.players[self.current_player].color
            self.current_player = (self.current_player + 1) % len(self.players)
            self.chips_count += 1
            if self.chips_count == 225:
                return None
            if self.is_bot:
                bot_move_pos = self.players[self.current_player].make_move()
                while self.map.map[bot_move_pos[0]][bot_move_pos[1]] is not None:
                    bot_move_pos = self.players[self.current_player].make_move()
                self.map.put_chip(self.players[self.current_player].color, bot_move_pos)
                if self.check_winner(bot_move_pos, self.players[self.current_player].color):
                    return self.players[self.current_player].color
                self.chips_count += 1
                self.current_player = 0
        return None
        '''
        if self.map.point_is_free(position):
            self.map.put_chip(self.players[self.current_player].color, position)
            self.chips_count += 1
            return self.check_winner(position, self.players[self.current_player].color)

    def check_winner(self, pos, color):
        self.current_player = (self.current_player + 1) % len(self.players)
        for direction in Const.directions:
            length = self.map.check_winner(pos[0], pos[1], direction, color, 1)
            if length >= 5:
                return color
