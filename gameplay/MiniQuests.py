from __future__ import annotations
from copy import deepcopy
from utilities.ItemInventory import Item
from gameplay.Entities import Entity, PlayerEntity
from utilities.WorldClock import WorldClock
from utilities.Primitives import RealmSize, Coordinate, Name, Description, Qty, QuestName

class Realm:
    def __init__(self, size: RealmSize):
        self.size = size
        self.grid: list[list[Entity | None]] = [[None for _ in range(int(size))] for _ in range(int(size))]
        self.player1: PlayerEntity = None
        self.player2: PlayerEntity = None

    def in_bounds(self, coord: Coordinate) -> bool:
        return self.size.in_bounds(coord)

    def place_entity(self, entity: Entity):
        if not self.in_bounds(entity.coord):
            raise ValueError(f"{entity.debug_print()} cannot be placed at ({entity.x}, {entity.y}) because it is out of bounds")

        # if self.grid[entity.x][entity.y] is not None:
        #     raise ValueError(f"{entity.debug_print()} cannot be placed at ({entity.x}, {entity.y}) because it is already occupied")

        if isinstance(entity, PlayerEntity):
            if self.player1 is None:
                self.player1 = entity
            elif self.player2 is None:
                self.player2 = entity

        self.grid[entity.x][entity.y] = entity
    
    def remove_entity(self, coord: Coordinate):
        if not self.in_bounds(coord):
            raise ValueError(f"Target ({coord.x}, {coord.y}) is out of bounds")
        
        if self.grid[coord.x][coord.y] is None:
            raise ValueError(f"Target ({coord.x}, {coord.y}) is not occupied")

        self.grid[coord.x][coord.y] = None

    def get_entity(self, coord: Coordinate) -> Entity | None:
        if not self.size.in_bounds(coord):
            raise ValueError(f"Target ({coord.x}, {coord.y}) is out of bounds")
        
        return self.grid[coord.x][coord.y]

    def move_entity(self, entity: Entity, direction: tuple[int, int]):
        if direction == (0, 0):
            return

        old_coord = entity.coord
        new_x = entity.coord.x + direction[0]
        new_y = entity.coord.y + direction[1]

        if new_x < 0 or new_y < 0:
            raise ValueError(f"Target ({new_x}, {new_y}) is out of bounds")

        new_coord = Coordinate(new_x, new_y)

        if not self.size.in_bounds(new_coord):
            raise ValueError(f"Target ({new_coord}) is out of bounds")

        entity_at_new = self.grid[new_coord.x][new_coord.y]
        if entity_at_new != None:
            if not entity_at_new.can_touch(entity):
                raise ValueError(f"{entity.debug_print()} cannot touch {entity_at_new.debug_print()}")

            entity_at_new.touch(entity)

        entity.move(direction)
        self.remove_entity(old_coord)
        self.place_entity(entity)

    def debug_print(self):
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
    
    def set_name(self, name: QuestName):
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
        self.reward = Item(
            Name("Stack of Cash"),
            Description("Reward for escorting the merchant"),
            Name("Common"))

    def check_lose(self) -> bool:
        return self.player1.dead or self.player2.dead

    def check_win(self) -> bool:
        return self.player1.win or self.player2.win

class CollectQuest(MiniQuest):
    def __init__(self, realm: Realm, target_count: Qty):
        super().__init__(realm)
        self.target_count = target_count
        self.reward = Item(
            Name("Crate of Apples"), 
            Description("Reward for collecting apples"), 
            Name("Common"))

    def check_lose(self) -> bool:
        return self.player1.dead or self.player2.dead

    def check_win(self) -> bool:
        return self.player1.score + self.player2.score >= self.target_count
