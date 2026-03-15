from __future__ import annotations
from gameplay.MiniQuests import MiniQuest
from utilities.WorldClock import WorldClock

# Gameplay/instance management loop/class
class Game:
    def __init__(self):
        self.mini_quest = None
        self.time = WorldClock.get_instance()

    def start_quest(self, quest: MiniQuest):
        self.mini_quest = quest

    def print_realm(self):
        self.mini_quest.realm.debug_print()

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
            try:
                self.print_realm()
                print(f"Time is currently {self.time.get_days()}:{self.time.get_hours()}:{self.time.get_minutes()}")
                p1_direction = input("Player 1 direction (w/a/s/d): ")
                p2_direction = input("Player 2 direction (w/a/s/d): ")
                p1_direction = self.input_to_direction(p1_direction)
                p2_direction = self.input_to_direction(p2_direction)
                self.mini_quest.process_turn(p1_direction, p2_direction)    
            except ValueError as e:
                print(e)
                print("Please enter a valid direction.")
                print()
                continue
        return self.mini_quest.check_lose(), self.mini_quest.check_win()



if __name__ == "__main__":
    from gameplay.MiniQuests import Realm, EscortQuest
    from gameplay.Entities import PlayerEntity, Target, Merchant, Lava

    realm = Realm(10)
    player1 = PlayerEntity(4, 4)
    player2 = PlayerEntity(5, 5)
    realm.place_entity(player1)
    realm.place_entity(player2)
    realm.place_entity(Target(0, 0))
    realm.place_entity(Merchant(9, 9))
    realm.place_entity(Lava(0, 9))



    game = Game(realm, player1, player2)
    game.start_quest(EscortQuest(realm, player1, player2))
    game.run()