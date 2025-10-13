import random
import json
from typing import List, Dict
from core import Human
from characters import Horoshist, Otlichnik, Starosta


class BossStrategy:

    def execute(self, boss: 'Boss', targets: List[Human]):
        pass


class AggressiveStrategy(BossStrategy):
    def execute(self, boss: 'Boss', targets: List[Human]):
        alive_targets = [t for t in targets if t.is_alive]
        if alive_targets:
            target = random.choice(alive_targets)
            boss.attack(target)


class AOEStrategy(BossStrategy):
    def execute(self, boss: 'Boss', targets: List[Human]):
        alive_targets = [t for t in targets if t.is_alive]
        print(f"{boss.name} дает очень сложные задания!")
        for target in alive_targets:
            damage = boss._strength // 2 + random.randint(5, 15)
            target.take_damage(damage)
            print(f"{target.name} получает {damage} урона")


class DebuffStrategy(BossStrategy):
    def execute(self, boss: 'Boss', targets: List[Human]):
        from effects import WEAKNESS
        alive_targets = [t for t in targets if t.is_alive]
        if alive_targets:
            target = random.choice(alive_targets)
            target.add_effect(WEAKNESS)
            print(f"{boss.name} выгоняет с пары {target.name}!")


class Boss(Human):
    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self._max_hp = 500 + level * 50
        self._hp = self._max_hp
        self._max_mp = 200 + level * 30
        self._mp = self._max_mp
        self._strength = 20 + level * 3
        self._agility = 12 + level
        self._intelligence = 15 + level * 2

        self._strategies = {
            'aggressive': AggressiveStrategy(),
            'aoe': AOEStrategy(),
            'debuff': DebuffStrategy()
        }
        self._current_strategy = 'aggressive'

    @property
    def phase(self) -> int:
        hp_percentage = self._hp / self._max_hp
        if hp_percentage > 0.7:
            return 1
        elif hp_percentage > 0.3:
            return 2
        else:
            return 3

    def _choose_strategy(self):
        if self.phase == 1:
            self._current_strategy = random.choice(['aggressive','aoe','debuff'])
        elif self.phase == 2:
            self._current_strategy = random.choice(['aggressive', 'aoe'])
        else:
            self._current_strategy = random.choice(['aoe', 'debuff'])

    def attack(self, target: Human):
        self._choose_strategy()
        strategy = self._strategies[self._current_strategy]
        return strategy

    def take_turn(self, party: List[Human]):
        strategy = self.attack(None)
        strategy.execute(self, party)


class Battle:
    def __init__(self, party: List[Human], boss: Boss, seed: int = None):
        self.party = party
        self.boss = boss
        self.turn_order = []
        self.current_turn = 0

        if seed is not None:
            random.seed(seed)

    def determine_turn_order(self):
        """Ходят по инициативе"""
        all_combatants = self.party + [self.boss]
        self.turn_order = sorted(
            all_combatants,
            key=lambda x: x.initiative,
            reverse=True
        )

    def is_battle_over(self) -> bool:
        """Проверяет, закончился ли бой"""
        party_alive = any(member.is_alive for member in self.party)
        boss_alive = self.boss.is_alive

        if not party_alive:
            print("Препод победил! Вы все отчислены!")
            return True
        elif not boss_alive:
            print("Пати победила!")
            return True
        return False

    def party_take_turn(self, character: Human):
        """Ход персонажа пати"""
        if not character.is_alive:
            return

        print(f"\n--- Ход {character.name} ---")
        character.process_effects()

        if isinstance(character, Starosta):
            wounded = [m for m in self.party if m.hp < m.max_hp * 0.7 and m.is_alive]
            if wounded and character.mp >= 15:
                target = min(wounded, key=lambda x: x.hp)
                print(f"{character.name} подсказывает {target.name}!")
                heal_amount = character._intelligence + random.randint(10, 20)
                target.heal(heal_amount)
                character._mp -= 15
            else:
                character.attack(self.boss)
        else:
            character.attack(self.boss)

    def next_turn(self):
        """Следующий ход в бою"""
        if not self.turn_order:
            self.determine_turn_order()

        if self.current_turn >= len(self.turn_order):
            self.current_turn = 0
            self.determine_turn_order()

        current_character = self.turn_order[self.current_turn]

        if current_character == self.boss:
            if self.boss.is_alive:
                print(f"\n--- Ход {self.boss.name} ---")
                self.boss.process_effects()
                self.boss.take_turn(self.party)
        else:
            self.party_take_turn(current_character)

        self.current_turn += 1

    def to_dict(self) -> Dict:
        """Сериализует состояние боя в словарь"""
        return {
            'party': [member.to_dict() for member in self.party],
            'boss': self.boss.to_dict(),
            'current_turn': self.current_turn
        }

    def save_to_file(self, filename: str):
        """Сохраняет состояние боя в JSON файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load_from_file(cls, filename: str, seed: int = None):
        """Загружает состояние боя из JSON-файла"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        party = []
        for char_data in data['party']:
            if char_data['class'] == 'Horoshist':
                char = Horoshist(char_data['name'], char_data['level'])
            elif char_data['class'] == 'Otlichnik':
                char = Otlichnik(char_data['name'], char_data['level'])
            elif char_data['class'] == 'Starosta':
                char = Starosta(char_data['name'], char_data['level'])
              
            char._hp = char_data['hp']
            char._max_hp = char_data['max_hp']
            char._mp = char_data['mp']
            char._max_mp = char_data['max_mp']

            party.append(char)

        boss_data = data['boss']
        boss = Boss(boss_data['name'], boss_data['level'])
        boss._hp = boss_data['hp']
        boss._max_hp = boss_data['max_hp']

        battle = cls(party, boss, seed)
        battle.current_turn = data['current_turn']

        return battle
