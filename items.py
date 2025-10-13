class Item:
    def __init__(self, name: str, item_type: str, value: int, description: str = ""):
        self.name = name
        self.item_type = item_type  # 'heal', 'mp_restore', 'buff', 'attack'
        self.value = value
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"

    def use(self, target):
        if self.item_type == 'heal':
            target.heal(self.value)
            print(f"{target.name} использует {self.name} и восстанавливает {self.value} HP")
        elif self.item_type == 'mp_restore':
            target.restore_mp(self.value)
            print(f"{target.name} использует {self.name} и восстанавливает {self.value} MP")


class Inventory:
    def __init__(self):
        self._items = []

    def add_item(self, item: Item):
        self._items.append(item)

    def remove_item(self, item: Item):
        self._items.remove(item)

    def get_items(self):
        return self._items.copy()

    def use_item(self, item_index: int, target):
        if 0 <= item_index < len(self._items):
            item = self._items[item_index]
            item.use(target)
            self.remove_item(item)
            return True
        return False


# Предопределенные предметы
ATTENDANCE= Item("100% посещаемость", "heal", 50, "Восстанавливает 50 HP")
NOTES = Item("Конспект", "mp_restore", 30, "Восстанавливает 30 MP")
