from __future__ import annotations
from copy import deepcopy
from utilities.ItemInventory import Item
from gameplay.Entities import Entity, PlayerEntity
from utilities.WorldClock import WorldClock


class Realm:
    def __init__(self, size: int):
        self.size = size
        self.grid: list[list[Entity | None]] = [[None for _ in range(size)] for _ in range(size)]
        self.player1: PlayerEntity = None
        self.player2: PlayerEntity = None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def place_entity(self, entity: Entity):
        if not self.in_bounds(entity.x, entity.y):
            raise ValueError(f"{entity.debug_print()} cannot be placed at ({entity.x}, {entity.y}) because it is out of bounds")

        # if self.grid[entity.x][entity.y] is not None:
        #     raise ValueError(f"{entity.debug_print()} cannot be placed at ({entity.x}, {entity.y}) because it is already occupied")

        if isinstance(entity, PlayerEntity):
            if self.player1 is None:
                self.player1 = entity
            elif self.player2 is None:
                self.player2 = entity

        self.grid[entity.x][entity.y] = entity
    
    def remove_entity(self, x: int, y: int):
        if not self.in_bounds(x, y):
            raise ValueError(f"Target ({x}, {y}) is out of bounds")
        
        if self.grid[x][y] is None:
            raise ValueError(f"Target ({x}, {y}) is not occupied")

        self.grid[x][y] = None

    def get_entity(self, x: int, y: int) -> Entity | None:
        if not self.in_bounds(x, y):
            raise ValueError(f"Target ({x}, {y}) is out of bounds")
        
        return self.grid[x][y]

    def move_entity(self, entity: Entity, direction: tuple[int, int]):
        if direction == (0, 0):
            return

        old_x = entity.x
        old_y = entity.y
        new_x = entity.x + direction[0]
        new_y = entity.y + direction[1]

        if not self.in_bounds(new_x, new_y):
            raise ValueError(f"Target ({new_x}, {new_y}) is out of bounds")

        if self.grid[new_x][new_y] is not None:
            if not self.grid[new_x][new_y].can_touch(entity):
                raise ValueError(f"{entity.debug_print()} cannot touch {self.grid[new_x][new_y].debug_print()}")

        if self.grid[new_x][new_y] is None:
            entity.move(direction)
            self.remove_entity(old_x, old_y)
            self.place_entity(entity)
        else:
            self.grid[new_x][new_y].touch(entity)
            entity.move(direction)
            self.remove_entity(old_x, old_y)
            self.place_entity(entity)

    def debug_print(self) -> str:
        for row in self.grid:
            for entity in row:
                if entity is None:
                    print(".", end="")
                else:
                    print(entity.debug_print(), end="")
            print()
        print()

# MiniQuest Parent/Root Class
class MiniQuest:
    def __init__(self, realm: Realm):
        self.original_realm = deepcopy(realm)
        self.realm = realm
        self.player1 = realm.player1
        self.player2 = realm.player2
        self.time = WorldClock.get_instance()
        self.name = None
        self.reward = None
    
    def set_name(self, name: str):
        self.name = name

    def tick(self):
        self.time.advance(0, 0, 10)

    def process_turn(self, p1_direction: tuple[int, int], p2_direction: tuple[int, int]):
        self.realm.move_entity(self.player1, p1_direction)
        self.realm.move_entity(self.player2, p2_direction)
        self.tick()

    def reset(self):
        self.realm = deepcopy(self.original_realm)
        self.player1 = self.realm.player1
        self.player2 = self.realm.player2

    def check_lose(self) -> bool:
        pass

    def check_win(self) -> bool:
        pass

# Implemented MiniQuest Formats
class EscortQuest(MiniQuest):
    def __init__(self, realm: Realm):
        super().__init__(realm)
        self.reward = Item("Stack of Cash", "Reward for escorting the merchant", "Common")

    def check_lose(self) -> bool:
        return self.player1.dead or self.player2.dead

    def check_win(self) -> bool:
        return self.player1.win or self.player2.win

class CollectQuest(MiniQuest):
    def __init__(self, realm: Realm, target_count: int):
        super().__init__(realm)
        self.target_count = target_count
        self.reward = Item("Crate of Apples", "Reward for collecting apples", "Common")

    def check_lose(self) -> bool:
        return self.player1.dead or self.player2.dead

    def check_win(self) -> bool:
        return self.player1.score + self.player2.score >= self.target_count