# Menu/flow for creating a quest
 
from utilities.World import World
from gameplay.MiniQuests import Realm, EscortQuest, CollectQuest
from gameplay.Entities import PlayerEntity, Target, Merchant, Lava, Water, Apple
 
# Entity display symbols and labels used in the placement menu
ENTITY_OPTIONS = {
    "escort": {
        "1": ("Player",    "P"),
        "2": ("Target",    "T"),
        "3": ("Merchant",  "M"),
        "4": ("Lava",      "L"),
        "5": ("Water",     "W"),
    },
    "collect": {
        "1": ("Player",    "P"),
        "2": ("Apple",     "A"),
        "3": ("Lava",      "L"),
        "4": ("Water",     "W"),
    },
}
 
 
class CreateQuest:
    def __init__(self, world: World):
        self.world = world
 
    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #
 
    def _get_realm_size(self) -> int:
        """Ask user for a valid realm size (4–20)."""
        while True:
            raw = input("  Enter realm size (4-20): ").strip()
            if raw.isdigit():
                size = int(raw)
                if 4 <= size <= 20:
                    return size
            print("  Please enter a number between 4 and 20.")
 
    def _get_quest_type(self) -> str:
        """Ask user to pick Escort or Collection."""
        while True:
            print("\n  Quest type:")
            print("  [1] Escort")
            print("  [2] Collection")
            choice = input("  Select (1/2): ").strip()
            if choice == "1":
                return "escort"
            elif choice == "2":
                return "collect"
            else:
                print("  Please enter 1 or 2.")
 
    def _get_quest_name(self) -> str:
        """Ask user for a non-empty quest name."""
        while True:
            name = input("  Quest name: ").strip()
            if name:
                return name
            print("  Name cannot be empty.")
 
    def _get_collect_target(self, apple_count: int) -> int:
        """Ask how many apples are needed to win (must be <= apples placed)."""
        while True:
            raw = input(f"  Apples to win (1-{apple_count}): ").strip()
            if raw.isdigit():
                n = int(raw)
                if 1 <= n <= apple_count:
                    return n
            print(f"  Please enter a number between 1 and {apple_count}.")
 
    def _print_grid(self, realm: Realm):
        """Print the current state of the realm grid."""
        print()
        # Column index header
        print("    " + " ".join(str(c % 10) for c in range(realm.size)))
        for r in range(realm.size):
            row_str = f"  {r % 10} "
            for c in range(realm.size):
                entity = realm.get_entity(r, c)
                if entity is None:
                    row_str += ". "
                else:
                    row_str += entity.debug_print() + " "
            print(row_str)
        print()
 
    def _print_entity_menu(self, quest_type: str):
        """Print the entity placement options for the current quest type."""
        print("  Entities:")
        for key, (label, symbol) in ENTITY_OPTIONS[quest_type].items():
            print(f"  [{key}] {label} ({symbol})")
        print("  [d] Done placing")
 
    def _place_entities(self, realm: Realm, quest_type: str):
        """
        Interactive loop: show grid, let user pick an entity and a coordinate,
        place it. Enforces exactly 2 PlayerEntities before allowing 'done'.
        """
        player_count = 0
 
        while True:
            self._print_grid(realm)
            print(f"  Players placed: {player_count}/2")
            self._print_entity_menu(quest_type)
 
            entity_choice = input("  Choose entity: ").strip().lower()
 
            if entity_choice == "d":
                if player_count < 2:
                    print("  You must place exactly 2 players before finishing.")
                    continue
                break
 
            options = ENTITY_OPTIONS[quest_type]
            if entity_choice not in options:
                print("  Invalid choice.")
                continue
 
            label, _ = options[entity_choice]
 
            # Get coordinates
            coords = input(f"  Place {label} at row,col (e.g. 3,5): ").strip()
            try:
                r_str, c_str = coords.split(",")
                row, col = int(r_str.strip()), int(c_str.strip())
            except ValueError:
                print("  Invalid coordinates. Use format: row,col")
                continue
 
            if not realm.in_bounds(row, col):
                print(f"  ({row},{col}) is out of bounds for a {realm.size}x{realm.size} realm.")
                continue
 
            # Build entity
            try:
                entity = self._build_entity(quest_type, entity_choice, row, col)
            except ValueError as e:
                print(f"  {e}")
                continue
 
            # Track player count
            if isinstance(entity, PlayerEntity):
                if player_count >= 2:
                    print("  Only 2 players are allowed.")
                    continue
                player_count += 1
 
            realm.place_entity(entity)
            print(f"  Placed {label} at ({row},{col}).")
 
        return realm
 
    def _build_entity(self, quest_type: str, choice: str, row: int, col: int):
        """Construct and return the correct Entity subclass."""
        if quest_type == "escort":
            mapping = {
                "1": PlayerEntity,
                "2": Target,
                "3": Merchant,
                "4": Lava,
                "5": Water,
            }
        else:  # collect
            mapping = {
                "1": PlayerEntity,
                "2": Apple,
                "3": Lava,
                "4": Water,
            }
        cls = mapping.get(choice)
        if cls is None:
            raise ValueError(f"Unknown entity choice: {choice}")
        return cls(row, col)
 
    def _count_entities(self, realm: Realm, entity_class) -> int:
        """Count how many entities of a given class are on the realm."""
        count = 0
        for row in realm.grid:
            for cell in row:
                if isinstance(cell, entity_class):
                    count += 1
        return count
 
    # ------------------------------------------------------------------ #
    #  Public run() entry point                                            #
    # ------------------------------------------------------------------ #
 
    def run(self):
        while True:
            print("\n" + "=" * 40)
            print("  Create Quest")
            print("=" * 40)
            print("  [1] Create new quest")
            print("  [2] Back to Main Menu")
            choice = input("\n  Select an option (1/2): ").strip()
 
            if choice == "2":
                break
            elif choice != "1":
                print("  Invalid option.")
                continue
 
            # Step 1: Quest type
            quest_type = self._get_quest_type()
 
            # Step 2: Realm size
            print()
            size = self._get_realm_size()
            realm = Realm(size)
 
            # Step 3: Place entities
            print("\n  Place your entities on the grid.")
            print("  (You must place exactly 2 Players.)\n")
            realm = self._place_entities(realm, quest_type)
 
            # Step 4: Quest name
            print()
            name = self._get_quest_name()
 
            # Step 5: Build the MiniQuest object
            if quest_type == "escort":
                quest = EscortQuest(realm)
            else:
                apple_count = self._count_entities(realm, Apple)
                if apple_count == 0:
                    print("  No apples were placed — defaulting win condition to 1.")
                    apple_count = 1
                target = self._get_collect_target(apple_count)
                quest = CollectQuest(realm, target)
 
            quest.set_name(name)
 
            # Step 6: Add to world
            self.world.quests.append(quest)
 
            print(f"\n  Quest '{name}' created and added to the quest list!")
            input("  Press Enter to continue...")