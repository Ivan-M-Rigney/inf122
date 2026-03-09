# Menu/flow for playing a quest

from gameplay.Game import Game
from utilities.World import World

class PlayQuest:
    def __init__(self, world: World):
        self.world = world
        self.quest = None
    
    def list_quests(self):
        questNum = 1
        for quest in self.world.quests:
            print(f'{questNum} - {quest.name}')
            questNum += 1
    
    def set_quest(self, choice: int):
        self.quest = self.world.quests[choice - 1]

    def run(self):
        game = Game()
        while True:
            # Present quests and choose one
            print("Which quest would you like to play?")
            self.list_quests()
            choice = int(input("Enter your choice: "))
            self.set_quest(choice)

            # Play selected quest
            game.start_quest(self.quest)
            (lose, win) = game.run()

            if lose:
                print("You lost the quest.")
                self.quest.reset()
            elif win:
                print("You won the quest.")
                self.world.player1.addQuest(self.quest)
                self.world.player1.addItem(self.quest.reward)
                self.world.player2.addQuest(self.quest)
                self.world.player2.addItem(self.quest.reward)
                print(f"You received {self.quest.reward.name}!")
                self.quest.reset()
            
            print("Would you like to play another quest? (y/n)")
            choice = input("Enter your choice: ")
            if choice == "y":
                continue
            else:
                print("Thank you for playing!")
                break
            
            
