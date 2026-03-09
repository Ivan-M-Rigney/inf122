from gameplay.MiniQuests import Realm
from gameplay.Entities import PlayerEntity, Target, Merchant, Lava, Apple
from gameplay.MiniQuests import EscortQuest, CollectQuest


escort_realm = Realm(10)
escort_player1 = PlayerEntity(4, 4)
escort_player2 = PlayerEntity(5, 5)
escort_realm.place_entity(escort_player1)
escort_realm.place_entity(escort_player2)
escort_realm.place_entity(Target(0, 0))
escort_realm.place_entity(Merchant(9, 9))
escort_realm.place_entity(Lava(0, 9))

base_escort_quest = EscortQuest(escort_realm)
base_escort_quest.set_name("Escort the Merchant")

collect_realm = Realm(10)
collect_player1 = PlayerEntity(4, 4)
collect_player2 = PlayerEntity(5, 5)
collect_realm.place_entity(collect_player1)
collect_realm.place_entity(collect_player2)
collect_realm.place_entity(Apple(0, 9))
collect_realm.place_entity(Apple(1, 9))
collect_realm.place_entity(Apple(2, 9))

base_collect_quest = CollectQuest(collect_realm, 3)
base_collect_quest.set_name("Collect 3 Apples")