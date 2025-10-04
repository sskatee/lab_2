from core import Effect
from typing import List, Optional


class Skill:
    def __init__(self, name: str, mp_cost: int, skill_type: str,
                 multiplier: float = 1.0, effect: Optional[Effect] = None, value: int = 0):
        self.name = name
        self.mp_cost = mp_cost
        self.skill_type = skill_type  # 'attack', 'heal', 'buff', 'debuff', 'aoe_attack', 'aoe_heal', 'shield'
        self.multiplier = multiplier
        self.effect = effect
        self.value = value

    def __str__(self):
        return f"{self.name} (MP: {self.mp_cost})"

    def can_use(self, user_mp: int) -> bool:
        return user_mp >= self.mp_cost
