from __future__ import annotations
from gameplay.MiniQuests import Realm
from gameplay.Entities import PlayerEntity, Target, Merchant, Lava, Apple, Water
from gameplay.MiniQuests import EscortQuest, CollectQuest
from utilities.Primitives import RealmSize, Coordinate


escort_realm = Realm(RealmSize(10))
escort_player1 = PlayerEntity(Coordinate(4, 0))
escort_player2 = PlayerEntity(Coordinate(5, 0))
escort_realm.place_entity(escort_player1)
escort_realm.place_entity(escort_player2)

escort_realm.place_entity(Target(Coordinate(0, 9)))
escort_realm.place_entity(Target(Coordinate(9, 9)))

escort_realm.place_entity(Merchant(Coordinate(2, 0)))
escort_realm.place_entity(Merchant(Coordinate(7, 0)))

escort_realm.place_entity(Lava(Coordinate(3, 0)))
escort_realm.place_entity(Lava(Coordinate(3, 1)))
escort_realm.place_entity(Lava(Coordinate(3, 2)))
escort_realm.place_entity(Lava(Coordinate(3, 3)))
escort_realm.place_entity(Lava(Coordinate(3, 4)))
escort_realm.place_entity(Lava(Coordinate(3, 5)))
escort_realm.place_entity(Water(Coordinate(3, 6)))

escort_realm.place_entity(Lava(Coordinate(6, 0)))
escort_realm.place_entity(Lava(Coordinate(6, 1)))
escort_realm.place_entity(Lava(Coordinate(6, 2)))
escort_realm.place_entity(Lava(Coordinate(6, 3)))
escort_realm.place_entity(Lava(Coordinate(6, 4)))
escort_realm.place_entity(Lava(Coordinate(6, 5)))
escort_realm.place_entity(Water(Coordinate(6, 6)))

escort_realm.place_entity(Lava(Coordinate(1, 6)))
escort_realm.place_entity(Lava(Coordinate(1, 7)))
escort_realm.place_entity(Lava(Coordinate(1, 8)))
escort_realm.place_entity(Lava(Coordinate(2, 8)))
escort_realm.place_entity(Lava(Coordinate(3, 8)))

escort_realm.place_entity(Lava(Coordinate(8, 6)))
escort_realm.place_entity(Lava(Coordinate(8, 7)))
escort_realm.place_entity(Lava(Coordinate(8, 8)))
escort_realm.place_entity(Lava(Coordinate(7, 8)))
escort_realm.place_entity(Lava(Coordinate(6, 8)))

base_escort_quest = EscortQuest(escort_realm)
base_escort_quest.set_name("Escort the Merchant")

collect_realm = Realm(RealmSize(10))
collect_player1 = PlayerEntity(Coordinate(0, 0))
collect_player2 = PlayerEntity(Coordinate(0, 9))
collect_realm.place_entity(collect_player1)
collect_realm.place_entity(collect_player2)

collect_realm.place_entity(Apple(Coordinate(0, 3)))
collect_realm.place_entity(Apple(Coordinate(3, 6)))
collect_realm.place_entity(Apple(Coordinate(4, 4)))
collect_realm.place_entity(Apple(Coordinate(5, 9)))
collect_realm.place_entity(Apple(Coordinate(7, 3)))
collect_realm.place_entity(Apple(Coordinate(9, 1)))
collect_realm.place_entity(Apple(Coordinate(7, 5)))
collect_realm.place_entity(Apple(Coordinate(9, 8)))

collect_realm.place_entity(Lava(Coordinate(4, 0)))
collect_realm.place_entity(Lava(Coordinate(4, 1)))
collect_realm.place_entity(Lava(Coordinate(4, 2)))

collect_realm.place_entity(Lava(Coordinate(3, 4)))
collect_realm.place_entity(Lava(Coordinate(3, 5)))

collect_realm.place_entity(Lava(Coordinate(4, 7)))
collect_realm.place_entity(Lava(Coordinate(4, 8)))
collect_realm.place_entity(Lava(Coordinate(4, 9)))

collect_realm.place_entity(Lava(Coordinate(6, 4)))
collect_realm.place_entity(Lava(Coordinate(7, 4)))

collect_realm.place_entity(Lava(Coordinate(8, 5)))
collect_realm.place_entity(Lava(Coordinate(9, 5)))


base_collect_quest = CollectQuest(collect_realm, 6)
base_collect_quest.set_name("Collect 6 Apples")
