class Vector(tuple):
    def __add__(self, other):
        return Vector([self.x + other.x, self.y + other.y])

    def __sub__(self, other):
        return Vector([self.x - other.x, self.y - other.y])

    def __mul__(self, value: int):
        return Vector([self.x * value, self.y * value])

    def __neg__(self):
        return Vector([-self.x, -self.y])

    @property
    def x(self):
        return super().__getitem__(0)

    @property
    def y(self):
        return super().__getitem__(1)
