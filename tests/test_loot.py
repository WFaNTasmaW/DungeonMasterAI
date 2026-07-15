from services.loot_service import LootService

service = LootService()

loot = service.generate(
    danger="5-10",
    features="Лаборатория алхимика"
)

print(loot.coins)
print()

print("Обычные предметы")
for item in loot.mundane_items:
    print(item)

print()

print("Камни")
for gem in loot.gems:
    print(gem)

print()

print("Магические")
for item in loot.magic_items:
    print(item)