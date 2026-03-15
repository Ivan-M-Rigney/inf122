from __future__ import annotations
from menus.PlayQuest import PlayQuest
from menus.PlayerInfo import PlayerInfo
from menus.CreateQuest import CreateQuest
from utilities.World import World
from utilities.Player import Player

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
player1 = Player(p1)
player2 = Player(p2) 

# CREATE WORLD OBJECT TODO
world = World(player1, player2)

# CREATE MENU OBJECTS TODO
# Example - PlayQuest(World)
playQuest = PlayQuest(world)
playerInfo = PlayerInfo(world)
createQuest = CreateQuest(world)

print(f"\nWelcome, {p1} and {p2}!")

# Instructions for later
print("\n" + "=" * 40)
print("  Instructions")
print("=" * 40)
print("\n  - You can input the number of the main menu option to select it.\n")
print("  - You are able to play a quest, create a quest, view player information, and quit the game.\n")
print("  - Please have fun!\n")

input("Press Enter to continue to the main menu:")

while True:
    print("\n" + "=" * 40)
    print("  Main Menu")
    print("=" * 40)
    print("  [1] Play a quest") # Play Quest
    print("  [2] Create a quest") # Play Quest
    print("  [3] Player Info") # Player Info
    print("  [4] Quit")

    choice = input("\nSelect an option (1/2/3/4): ").strip()

    if choice == "1":
        print("\nStarting Play Quest Menu...\n")
        playQuest.run()

    elif choice == "2":
        print("\nStarting Create Quest Menu...\n")
        createQuest.run()

    elif choice == "3":
        print("\nStarting Player Info Menu...\n")
        playerInfo.run()

    elif choice == "4":
        print(f"\n  Farewell, {p1} and {p2}!\n")
        break

    else:
        print("  Invalid option. Please enter 1, 2, 3, or 4.")