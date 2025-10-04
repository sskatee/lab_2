from core import Effect

POISON = Effect("Яд", 3, "dot", 5)
REGENERATION = Effect("Регенерация", 3, "hot", 8)
SHIELD = Effect("Щит", 2, "shield", 20)
WEAKNESS = Effect("Слабость", 2, "debuff", -3)
STRENGTH = Effect("Сила", 3, "buff", 5)

EFFECTS_DICT = {
    "poison": POISON,
    "regeneration": REGENERATION,
    "shield": SHIELD,
    "weakness": WEAKNESS,
    "strength": STRENGTH
}
