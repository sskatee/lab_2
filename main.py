from characters import Horoshist, Otlichnik, Starosta
from battle import Battle, Boss
import random


def create_party():
    party = [
        Horoshist("Хорошист"),
        Otlichnik("Отличник"),
        Starosta("Староста")
    ]
    return party


def main():
    print("= Адская сессия =")
    print("1. Начать новую игру")
    print("2. Загрузить игру")

    choice = input("Выберите опцию: ")

    if choice == "1":
        seed = input("Введите seed для генератора случайных чисел (или оставьте пустым): ")
        if seed:
            random.seed(int(seed))

        difficulty = input("Выберите сложность (1-легкая, 2-средняя, 3-сложная): ")
        level = int(difficulty) if difficulty in ['1', '2', '3'] else 2

        party = create_party()
        boss = Boss("Злой препод", level)

        battle = Battle(party, boss)

    elif choice == "2":
        filename = input("Введите имя файла для загрузки: ")
        try:
            battle = Battle.load_from_file(filename)
        except FileNotFoundError:
            print("Файл не найден!")
            return
    else:
        print("Неверный выбор!")
        return

    while not battle.is_battle_over():
        battle.next_turn()

        print("\n--- Состояние боя ---")
        for member in battle.party:
            print(f"{member.name}: HP {member.hp}/{member.max_hp}, MP {member.mp}/{member.max_mp}")
        print(f"{battle.boss.name}: HP {battle.boss.hp}/{battle.boss.max_hp}")

        save = input("\nСохранить игру? (y/n): ")
        if save.lower() == 'y':
            filename = input("Введите имя файла: ")
            battle.save_to_file(filename)
            print("Игра сохранена!")

        input("Нажмите Enter для следующего хода...")

    print("Игра окончена!")


if __name__ == "__main__":
    main()
