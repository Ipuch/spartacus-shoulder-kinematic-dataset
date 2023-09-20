from enum import Enum


class Hello(Enum):
    WORLD = 1
    UNIVERSE = 2

    @property
    def string(self):
        if self == Hello.WORLD:
            return "world"
        elif self == Hello.UNIVERSE:
            return "universe"
        else:
            raise ValueError("This should never happen")


hello = Hello.UNIVERSE
print(hello.string)
print(hello.string)

