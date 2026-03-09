from utilities.Player import Player
from gameplay.BaseQuests import base_escort_quest, base_collect_quest

class World:
    def __init__(self, player1: Player, player2: Player):
        self.quests = [base_escort_quest, base_collect_quest]
        self.player1 = player1
        self.player2 = player2