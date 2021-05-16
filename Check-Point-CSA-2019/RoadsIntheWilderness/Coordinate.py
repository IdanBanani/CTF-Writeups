from collections import namedtuple


class Coordinate(namedtuple("Coordinate", ["x", "y"])):
    __slots__ = ()

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return (self.x == other.x) and (self.y == other.y)
        return False

    def __hash__(self):
        return hash(self.x) * hash(self.y)