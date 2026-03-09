from utilities.ItemInventory import Inventory, Item

class Player:
    def __init__(self, username: str):
        self.username = username
        self.quests_completed = []
        self.inventory = Inventory()
    
    def addItem(self, item: Item):
        self.inventory.addItem(item)
    
    def addQuest(self, quest):
        self.quests_completed.append(quest)