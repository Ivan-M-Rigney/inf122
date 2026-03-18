from __future__ import annotations
from utilities.Primitives import Name, Description

class Item:
    def __init__(self, name: Name, description: Description, rarity: Name): # Rarity ENUM changed to string for simplicity
        self.name = name
        self.description = description
        self.rarity = rarity

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
# End of Code from Ivan's A3
