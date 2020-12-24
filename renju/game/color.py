from enum import Enum
from colormap import rgb2hex
from colormap import hex2rgb


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 128, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 20, 147)
    BROWN = (139, 69, 19)

    @staticmethod
    def toRGB(rgb_color: tuple):
        return rgb2hex(rgb_color[0], rgb_color[1], rgb_color[2])

    @staticmethod
    def fromRGB(hex_color: str):
        return hex2rgb(hex_color)
