from __future__ import annotations

class Entity:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hidden = False
    
    def can_touch(self, other: "Entity") -> bool:
        pass
    
    def touch(self, other: "Entity"):
        pass

    def move(self, direction: tuple[int, int]):
        self.x += direction[0]
        self.y += direction[1]

class Tile(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def debug_print(self) -> str:
        return "."

class PlayerEntity(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.dead = False
        self.stuck = False
        self.score = 0
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
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def touch(self, other: "Entity"):
        if isinstance(other, PlayerEntity):
            other.dead = True

    def debug_print(self) -> str:
        return "L"

class Water(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def touch(self, other: "Entity"):
        print("You stepped into the water and got wet!")

    def debug_print(self) -> str:
        return "W"

class Apple(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def touch(self, other: "Entity"):
        if isinstance(other, PlayerEntity):
            other.score += 1
            self.hidden = True

    def debug_print(self) -> str:
        return "A"

class Merchant(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def touch(self, other: "Entity"):
        if isinstance(other, PlayerEntity):
            other.companion = self
            self.hidden = True

    def debug_print(self) -> str:
        return "M"

class Target(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def can_touch(self, other: "Entity") -> bool:
        return True
    
    def touch(self, other: "Entity"):
        if isinstance(other, PlayerEntity):
            if isinstance(other.companion, Merchant):
                other.win = True

    def debug_print(self) -> str:
        return "T"