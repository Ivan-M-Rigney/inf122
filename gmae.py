

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
    print("  [1] Escort Quest")
    print("  [2] Collect Quest")
    print("  [3] Settings")
    print("  [4] Quit")

    choice = input("\nSelect an option (1/2/3): ").strip()

    if choice == "1":
        print("\n  [Escort Quest coming soon]\n")

    elif choice == "2":
        print("\n  [Collect Quest coming soon]\n")

    elif choice == "3":
            print("\n  [Settings coming soon]\n")

    elif choice == "4":
        print(f"\n  Farewell, {p1} and {p2}!\n")
        break

    else:
        print("  Invalid option. Please enter 1, 2, or 3.")