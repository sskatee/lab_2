import random
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class Effect:
    def __init__(self, name: str, duration: int, effect_type: str, value: int = 0):
        self.name = name
        self.duration = duration
        self.effect_type = effect_type  # 'buff', 'debuff', 'dot', 'hot', 'shield'
        self.value = value

    def __str__(self):
        return f"{self.name} ({self.duration} turns)"

    def to_dict(self):
        return {
            'name': self.name,
            'duration': self.duration,
            'effect_type': self.effect_type,
            'value': self.value
        }


class Human(ABC):
    def __init__(self, name: str, level: int = 1):
        self._name = name
        self._level = level
        self._max_hp = 100
        self._hp = self._max_hp
        self._max_mp = 50
        self._mp = self._max_mp
        self._strength = 10
        self._agility = 10
        self._intelligence = 10
        self._effects: List[Effect] = []
        self._inventory = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def max_hp(self) -> int:
        return self._max_hp

    @property
    def mp(self) -> int:
        return self._mp

    @property
    def max_mp(self) -> int:
        return self._max_mp

    @property
    def is_alive(self) -> bool:
        return self._hp > 0

    @property
    def initiative(self) -> int:
        return self._agility + random.randint(1, 10)

    def take_damage(self, damage: int):
        self._hp = max(0, self._hp - damage)

    def heal(self, amount: int):
        self._hp = min(self._max_hp, self._hp + amount)

    def restore_mp(self, amount: int):
        self._mp = min(self._max_mp, self._mp + amount)

    def add_effect(self, effect: Effect):
        self._effects.append(effect)

    def process_effects(self):
        new_effects = []
        for effect in self._effects:
            effect.duration -= 1
            if effect.duration > 0:
                new_effects.append(effect)

            if effect.effect_type == 'dot':
                self.take_damage(effect.value)
                print(f"{self.name} получает {effect.value} урона от {effect.name}")
            elif effect.effect_type == 'hot':
                self.heal(effect.value)
                print(f"{self.name} восстанавливает {effect.value} HP от {effect.name}")

        self._effects = new_effects

    @abstractmethod
    def attack(self, target: 'Human'):
        pass

    def __str__(self):
        return f"{self._name} (HP: {self._hp}/{self._max_hp}, MP: {self._mp}/{self._max_mp})"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._name}', level={self._level})"

    def to_dict(self):
        return {
            'class': self.__class__.__name__,
            'name': self._name,
            'level': self._level,
            'hp': self._hp,
            'max_hp': self._max_hp,
            'mp': self._mp,
            'max_mp': self._max_mp,
            'strength': self._strength,
            'agility': self._agility,
            'intelligence': self._intelligence,
            'effects': [effect.to_dict() for effect in self._effects]
        }
