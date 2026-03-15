from __future__ import annotations
from gameplay.MiniQuests import Realm
from gameplay.Entities import PlayerEntity, Target, Merchant, Lava, Apple, Water
from gameplay.MiniQuests import EscortQuest, CollectQuest


escort_realm = Realm(10)
escort_player1 = PlayerEntity(4, 0)
escort_player2 = PlayerEntity(5, 0)
escort_realm.place_entity(escort_player1)
escort_realm.place_entity(escort_player2)

escort_realm.place_entity(Target(0, 9))
escort_realm.place_entity(Target(9, 9))

escort_realm.place_entity(Merchant(2, 0))
escort_realm.place_entity(Merchant(7, 0))

escort_realm.place_entity(Lava(3, 0))
escort_realm.place_entity(Lava(3, 1))
escort_realm.place_entity(Lava(3, 2))
escort_realm.place_entity(Lava(3, 3))
escort_realm.place_entity(Lava(3, 4))
escort_realm.place_entity(Lava(3, 5))
escort_realm.place_entity(Water(3, 6))

escort_realm.place_entity(Lava(6, 0))
escort_realm.place_entity(Lava(6, 1))
escort_realm.place_entity(Lava(6, 2))
escort_realm.place_entity(Lava(6, 3))
escort_realm.place_entity(Lava(6, 4))
escort_realm.place_entity(Lava(6, 5))
escort_realm.place_entity(Water(6, 6))

escort_realm.place_entity(Lava(1, 6))
escort_realm.place_entity(Lava(1, 7))
escort_realm.place_entity(Lava(1, 8))
escort_realm.place_entity(Lava(2, 8))
escort_realm.place_entity(Lava(3, 8))

escort_realm.place_entity(Lava(8, 6))
escort_realm.place_entity(Lava(8, 7))
escort_realm.place_entity(Lava(8, 8))
escort_realm.place_entity(Lava(7, 8))
escort_realm.place_entity(Lava(6, 8))

base_escort_quest = EscortQuest(escort_realm)
base_escort_quest.set_name("Escort the Merchant")

collect_realm = Realm(10)
collect_player1 = PlayerEntity(0, 0)
collect_player2 = PlayerEntity(0, 9)
collect_realm.place_entity(collect_player1)
collect_realm.place_entity(collect_player2)

collect_realm.place_entity(Apple(0, 3))
collect_realm.place_entity(Apple(3, 6))
collect_realm.place_entity(Apple(4, 4))
collect_realm.place_entity(Apple(5, 9))
collect_realm.place_entity(Apple(7, 3))
collect_realm.place_entity(Apple(9, 1))
collect_realm.place_entity(Apple(7, 5))
collect_realm.place_entity(Apple(9, 8))

collect_realm.place_entity(Lava(4, 0))
collect_realm.place_entity(Lava(4, 1))
collect_realm.place_entity(Lava(4, 2))

collect_realm.place_entity(Lava(3, 4))
collect_realm.place_entity(Lava(3, 5))

collect_realm.place_entity(Lava(4, 7))
collect_realm.place_entity(Lava(4, 8))
collect_realm.place_entity(Lava(4, 9))

collect_realm.place_entity(Lava(6, 4))
collect_realm.place_entity(Lava(7, 4))

collect_realm.place_entity(Lava(8, 5))
collect_realm.place_entity(Lava(9, 5))


base_collect_quest = CollectQuest(collect_realm, 6)
base_collect_quest.set_name("Collect 6 Apples")