from knowledge.loaders import SpellLoader

spells = SpellLoader().load()

for spell in spells:
    if "Ускорение" in spell.name:
        print(spell.name)
        print(spell.url)
        break
else:
    print("НЕ НАЙДЕНО")