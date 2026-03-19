from __future__ import annotations
from utilities.Primitives import Coordinate, Qty

class Entity:
    def __init__(self, coord: Coordinate):
        self.coord = coord
        self.hidden = False

    @property
    def x(self) -> int:
        return self.coord.x

    @property
    def y(self) -> int:
        return self.coord.y
    
    def can_touch(self, other: "Entity") -> bool:
        pass
    
    def touch(self, other: "Entity"):
        pass

    def move(self, direction: tuple[int, int]):
        self.coord = Coordinate(self.coord.x + direction[0], self.coord.y + direction[1])
     
    def debug_print(self) -> str:
        return " "

class Tile(Entity):
    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def debug_print(self) -> str:
        return "."

class PlayerEntity(Entity):
    def __init__(self, coord: Coordinate):
        super().__init__(coord)
        self.dead = False
        self.stuck = False
        self.score = Qty(0)
        self.companion = None
        self.win = False
    
    def can_touch(self, other: "Entity") -> bool:
        return False

    def debug_print(self) -> str:
        if self.companion is None:
            return "P"
        else:
            return "E"

class Lava(Entity):
    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def touch(self, other: "Entity"):
        if isinstance(other, PlayerEntity):
            other.dead = True

    def debug_print(self) -> str:
        return "L"

class Water(Entity):
    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def touch(self, other: "Entity"):
        print("You stepped into the water and got wet!")

    def debug_print(self) -> str:
        return "W"

class Apple(Entity):
    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def touch(self, other: "Entity"):
        if isinstance(other, PlayerEntity):
            other.score += 1
            self.hidden = True

    def debug_print(self) -> str:
        return "A"

class Merchant(Entity):
    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def touch(self, other: "Entity"):
        if isinstance(other, PlayerEntity):
            other.companion = self
            self.hidden = True

    def debug_print(self) -> str:
        return "M"

class Target(Entity):
    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def touch(self, other: "Entity"):
        if isinstance(other, PlayerEntity):
            if isinstance(other.companion, Merchant):
                other.win = True

    def debug_print(self) -> str:
        return "T"
