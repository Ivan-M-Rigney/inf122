from entities import *


class Realm:
    def __init__(self, size: int):
        self.size = size
        self.grid: list[list[Entity | None]] = [[None for _ in range(size)] for _ in range(size)]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def place_entity(self, entity: Entity):
        if not self.in_bounds(entity.x, entity.y):
            raise ValueError(f"Entity ({entity.x}, {entity.y}) is out of bounds")
        
        if self.grid[entity.x][entity.y] is not None:
            raise ValueError(f"Entity ({entity.x}, {entity.y}) is already occupied")

        self.grid[entity.x][entity.y] = entity
    
    def remove_entity(self, x: int, y: int):
        if not self.in_bounds(x, y):
            raise ValueError(f"Entity ({x}, {y}) is out of bounds")
        
        if self.grid[x][y] is None:
            raise ValueError(f"Entity ({x}, {y}) is not occupied")

        self.grid[x][y] = None

    def get_entity(self, x: int, y: int) -> Entity | None:
        if not self.in_bounds(x, y):
            raise ValueError(f"Entity ({x}, {y}) is out of bounds")
        
        return self.grid[x][y]

    def move_entity(self, entity: Entity, direction: tuple[int, int]):
        if direction == (0, 0):
            return

        old_x = entity.x
        old_y = entity.y
        new_x = entity.x + direction[0]
        new_y = entity.y + direction[1]

        if not self.in_bounds(new_x, new_y):
            raise ValueError(f"Entity ({entity.x}, {entity.y}) is out of bounds")

        if self.grid[new_x][new_y] is not None:
            if not self.grid[new_x][new_y].can_touch(entity):
                raise ValueError(f"Entity ({entity.x}, {entity.y}) cannot touch entity ({new_x}, {new_y})")

        if self.grid[new_x][new_y] is None:
            entity.move(direction)
            self.grid[new_x][new_y] = entity
            self.remove_entity(old_x, old_y)
        else:
            self.grid[new_x][new_y].touch(entity)
            entity.move(direction)
            self.grid[new_x][new_y] = entity
            self.remove_entity(old_x, old_y)

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
    def __init__(self, realm: Realm, player1: Player, player2: Player):
        self.realm = realm
        self.player1 = player1
        self.player2 = player2
        self.time = 0
        self.over = False

    def tick(self):
        self.time += 1

    def process_turn(self, p1_direction: tuple[int, int], p2_direction: tuple[int, int]):
        self.realm.move_entity(self.player1, p1_direction)
        self.realm.move_entity(self.player2, p2_direction)
        self.tick()

    def check_lose(self) -> bool:
        pass

    def check_win(self) -> bool:
        pass

# Implemented MiniQuest Formats
class EscortQuest(MiniQuest):
    def __init__(self, realm: Realm, player1: Player, player2: Player):
        super().__init__(realm, player1, player2)

    def check_lose(self) -> bool:
        return self.player1.dead or self.player2.dead

    def check_win(self) -> bool:
        return self.player1.win or self.player2.win

class CollectQuest(MiniQuest):
    def __init__(self, realm: Realm, player1: Player, player2: Player, target_count: int):
        super().__init__(realm, player1, player2)
        self.target_count = target_count

    def check_lose(self) -> bool:
        return self.player1.dead or self.player2.dead

    def check_win(self) -> bool:
        return self.player1.score + self.player2.score >= self.target_count
        
# Gameplay/instance management loop/class
class Game:
    def __init__(self, realm: Realm, player1: Player, player2: Player):
        self.realm = realm
        self.player1 = player1
        self.player2 = player2
        self.mini_quest = None

    def start_quest(self, quest: MiniQuest):
        self.mini_quest = quest

    # Debug testing loop for time being

    def input_to_direction(self, input: str) -> tuple[int, int]:
        if input == "w":
            return (-1, 0)
        elif input == "a":
            return (0, -1)
        elif input == "s":
            return (1, 0)
        elif input == "d":
            return (0, 1)
        elif input == "q":
            return (0, 0)
        else:
            raise ValueError(f"Invalid input: {input}")
    
    def run(self):
        while not self.mini_quest.check_lose() and not self.mini_quest.check_win():
            p1_direction = input("Player 1 direction (w/a/s/d): ")
            p2_direction = input("Player 2 direction (w/a/s/d): ")
            p1_direction = self.input_to_direction(p1_direction)
            p2_direction = self.input_to_direction(p2_direction)

            self.mini_quest.process_turn(p1_direction, p2_direction)
            print(self.realm.debug_print())
            
        return self.mini_quest.check_lose(), self.mini_quest.check_win()

if __name__ == "__main__":
    realm = Realm(10)
    player1 = Player(4, 4)
    player2 = Player(5, 5)
    realm.place_entity(player1)
    realm.place_entity(player2)
    realm.place_entity(Target(0, 0))
    realm.place_entity(Merchant(9, 9))
    realm.place_entity(Lava(0, 9))



    game = Game(realm, player1, player2)
    game.start_quest(EscortQuest(realm, player1, player2))
    game.run()