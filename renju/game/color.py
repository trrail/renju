class Color:
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 128, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        self.purple = (128, 0, 128)
        self.pink = (255, 20, 147)
        self.brown = (139, 69, 19)
        self.point = 0
        self.colors = [self.black, self.white,
                       self.green, self.red,
                       self.blue, self.yellow,
                       self.purple, self.pink,
                       self.brown]
        self.colors_next_to_current = []
        self._prepare_next_colors_dict()

    def next_color(self, max_count_of_colors: int) -> tuple:
        if self.point + 1 >= max_count_of_colors:
            self.point = 0
        else:
            self.point += 1
        return self.colors[self.point - 1]

    def _prepare_next_colors_dict(self):
        current_color = self.next_color(9)
        for i in range(9):
            next_color = self.next_color(9)
            self.colors_next_to_current.append((current_color, next_color))
            current_color = next_color

    def next_to_current_color(self, color: tuple):
        for colors in self.colors_next_to_current:
            if color == colors[0]:
                return colors[1]

    def reset(self):
        self.point = 0
