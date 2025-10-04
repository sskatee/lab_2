from core import Human, Effect
from skills import Skill
import random


class Warrior(Human):
    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self._max_hp = 150 + level * 20
        self._hp = self._max_hp
        self._max_mp = 30 + level * 5
        self._mp = self._max_mp
        self._strength = 15 + level * 2
        self._agility = 8 + level
        self._intelligence = 5 + level

        self.skills = [
            Skill("Сильная атака", 10, "attack", multiplier=1.5),
            Skill("Размашистый удар", 15, "aoe_attack", multiplier=1.2),
            Skill("Берсерк", 20, "self_buff", effect=Effect("Берсерк", 3, "buff", 5))
        ]

    def attack(self, target: Human):
        base_damage = self._strength + random.randint(1, 5)
        # Шанс крита 20%
        if random.random() < 0.2:
            base_damage *= 2
            print(f"Критический удар! {self.name} наносит {base_damage} урона!")
        else:
            print(f"{self.name} атакует {target.name} и наносит {base_damage} урона")
        target.take_damage(base_damage)


class Mage(Human):
    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self._max_hp = 80 + level * 10
        self._hp = self._max_hp
        self._max_mp = 80 + level * 15
        self._mp = self._max_mp
        self._strength = 5 + level
        self._agility = 7 + level
        self._intelligence = 18 + level * 2

        self.skills = [
            Skill("Огненный шар", 15, "attack", multiplier=2.0),
            Skill("Ледяная стрела", 10, "attack", effect=Effect("Заморозка", 2, "debuff")),
            Skill("Щит маны", 20, "shield", value=30)
        ]

    def attack(self, target: Human):
        base_damage = self._intelligence + random.randint(3, 8)
        print(f"{self.name} бросает магический снаряд в {target.name} и наносит {base_damage} урона")
        target.take_damage(base_damage)


class Healer(Human):
    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self._max_hp = 100 + level * 12
        self._hp = self._max_hp
        self._max_mp = 70 + level * 12
        self._mp = self._max_mp
        self._strength = 6 + level
        self._agility = 9 + level
        self._intelligence = 14 + level * 2

        self.skills = [
            Skill("Лечение", 15, "heal", multiplier=1.5),
            Skill("Массовое лечение", 25, "aoe_heal", multiplier=1.0),
            Skill("Благословение", 20, "buff", effect=Effect("Благословение", 3, "buff", 3))
        ]

    def attack(self, target: Human):
        base_damage = max(self._strength, self._intelligence // 2) + random.randint(2, 6)
        print(f"{self.name} атакует {target.name} и наносит {base_damage} урона")
        target.take_damage(base_damage)
