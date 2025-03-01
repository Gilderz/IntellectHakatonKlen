from ursina import *

class Inventory:
    def __init__(self):
        self.inventory_active = False
        self.items = []  # Список для зберігання предметів у інвентарі

        # Створення інвентаря
        self.inventory = Entity(
            parent=camera.ui,  # Прив'язка до інтерфейсу камери
            model='quad',  # Модель для фону інвентаря
            scale=(1.0, 0.5),  # Розмір інвентаря (10x5 комірок)
            color=color.dark_gray,  # Колір фону
            position=(0, 0),  # Центруємо інвентар на екрані
            enabled=False  # Спочатку інвентар прихований
        )

        # Створення сітки інвентаря (10x5 комірок, всього 50 комірок)
        self.cell_size = 0.1  # Розмір комірки
        self.inventory_grid = []
        for y in range(5):  # 5 рядків
            for x in range(10):  # 10 стовпців
                cell = Entity(
                    parent=self.inventory,
                    model='quad',
                    color=color.white,
                    scale=(self.cell_size, self.cell_size),
                    x=-0.45 + x * (self.cell_size + 0.02),  # Розташування комірки по горизонталі
                    y=0.2 - y * (self.cell_size + 0.02),  # Розташування комірки по вертикалі
                    alpha=0.5  # Прозорість комірки
                )
                self.inventory_grid.append(cell)

    # Функція для перемикання стану інвентаря
    def toggle_inventory(self):
        self.inventory_active = not self.inventory_active
        self.inventory.enabled = self.inventory_active
        return not self.inventory_active  # Повертаємо стан управління гравцем

    # Функція для додавання предмету до інвентаря
    def add_item(self, item):
        if len(self.items) < 50:  # Перевіряємо, чи є вільні комірки
            self.items.append(item)
            print(f"Added item: {item}")
        else:
            print("Inventory is full!")

    # Функція для видалення предмету з інвентаря
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed item: {item}")
        else:
            print("Item not found in inventory!")