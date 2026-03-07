from WorldClock import WorldClock

profiles = {}

print("=" * 50)
print("Welcome to GuildQuest Adventure!")
print("=" * 50)

# Player 1 username
while True:
    p1 = input("\nEnter username for Player 1: ").strip()
    if not p1:
        print("Username cannot be empty.")
        continue
    profiles[p1] = {"username": p1, "quests_completed": [], "inventory": []}
    break

# Player 2 username
while True:
    p2 = input("Enter username for Player 2: ").strip()
    if not p2:
        print("Username cannot be empty.")
        continue
    if p2 == p1:
        print("That username is already taken by Player 1. Choose a different one.")
        continue
    profiles[p2] = {"username": p2, "quests_completed": [], "inventory": []}
    break

# CREATE PLAYER OBJECTS TODO

# CREATE WORLD OBJECT TODO

# CREATE MENU OBJECTS TODO
# Example - PlayQuest(World)
# Example - PlayerInfo(World)
# Example - CreateQuest(World)

print(f"\nWelcome, {p1} and {p2}!")

# Instructions for later
print("\n" + "=" * 40)
print("  Instructions")
print("=" * 40)
print("\n  [Coming soon]\n")

input("Press Enter to continue to the main menu:")

while True:
    print("\n" + "=" * 40)
    print("  Main Menu")
    print("=" * 40)
    print("  [1] Escort Quest") # Play Quest
    print("  [2] Collect Quest") # Player Info
    print("  [3] Settings") # Create Quest
    print("  [4] Quit")

    choice = input("\nSelect an option (1/2/3): ").strip()

    if choice == "1":
        print("\n  [Escort Quest coming soon]\n")
        # PlayQuest.run()

    elif choice == "2":
        print("\n  [Collect Quest coming soon]\n")
        # PlayerInfo.run()

    elif choice == "3":
        print("\n  [Settings coming soon]\n")
        # CreateQuest.run()

    elif choice == "4":
        print(f"\n  Farewell, {p1} and {p2}!\n")
        break

    else:
        print("  Invalid option. Please enter 1, 2, or 3.")


# Ideas

class World:
    def __init__(self, player1: Player, player2: Player):
        self.quests = []
        self.player1 = player1
        self.player2 = player2
        self.time = WorldClock()

class Player:
    def __init__(self, username: str):
        self.username = username
        self.quests_completed = []
        self.inventory = Inventory()
    
    def addItem(self, item: Item):
        self.inventory.addItem(item)
    
    def addQuest(self, quest):
        self.quests.append(quest)

# Code from Ivan's A3
class Inventory:
    def __init__(self):
        self.maxCapacity = 100
        self.items = []

    def addItem(self, item: Item):
        if len(self.items) < self.maxCapacity:
            self.items.append(item)
        else:
            raise Exception("Inventory is full")
    
    def updateItem(self, item: int, newItem: Item):
        if item < len(self.items):
            self.items[item] = newItem
        else:
            raise Exception("Item index out of bounds")

    def removeItem(self, item: int):
        self.items.pop(item)

    # Refactoring #1: Extract Method
    def viewInventory(self):
        for item in self.items:
            print(item.name, ' - ', item.description, ' - ', item.rarity)

class Item:
    def __init__(self, name: str, description: str, rarity: Rarity):
        self.name = name
        self.description = description
        self.rarity = rarity
# End of Code from Ivan's A3