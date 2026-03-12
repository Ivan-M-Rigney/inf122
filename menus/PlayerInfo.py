# Menu/flow for viewing player information

from utilities.World import World

class PlayerInfo:
    def __init__(self, world: World):
        self.world = world

    def _show_player(self, player):
        print("\n" + "-" * 40)
        print(f"  {player.username}")
        print("-" * 40)
        print("\n  Stats")
        print("  -----")
        print(f"  Quests completed: {len(player.quests_completed)}")
        if player.quests_completed:
            for i, q in enumerate(player.quests_completed, 1):
                name = getattr(q, 'name', 'Unknown quest')
                print(f"    {i}. {name}")
        print("\n  Inventory")
        print("  --------")
        if not player.inventory.items:
            print("  (empty)")
        else:
            for item in player.inventory.items:
                print(f"    - {item.name} | {item.description} | {item.rarity}")
        print()

    def run(self):
        while True:
            print("\n" + "=" * 40)
            print("  Player Info")
            print("=" * 40)
            print("  [1] Player 1 -", self.world.player1.username)
            print("  [2] Player 2 -", self.world.player2.username)
            print("  [3] Back to Main Menu")
            choice = input("\nSelect an option (1/2/3): " ).strip()

            if choice == "1":
                self._show_player(self.world.player1)
            elif choice == "2":
                self._show_player(self.world.player2)
            elif choice == "3":
                break
            else:
                print("  Invalid option. Please enter 1, 2, or 3.")

            if choice in ("1", "2"):
                input("Press Enter to continue...")
