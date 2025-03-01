from ursina import *

class Hotbar:
    def __init__(self):
        self.hotbar = Entity(
            parent=camera.ui,
            model='quad',
            scale=(0.6, 0.1),
            y=-0.45,  # Позиція внизу екрану
            color=color.gray
        )

        # Блоки для хотбару
        self.blocks = [
            {"color": color.red, "name": "Red Block"},
            {"color": color.blue, "name": "Blue Block"},
            {"color": color.yellow, "name": "Yellow Block"}
        ]

        # Відображення блоків у хотбарі
        self.hotbar_slots = []
        for i, block in enumerate(self.blocks):
            slot = Button(
                parent=self.hotbar,
                model='cube',
                color=block["color"],
                scale=(0.1, 0.1),
                x=-0.25 + i * 0.25,  # Розташування слотів
                text=str(i + 1),  # Відображення цифри для вибору
                on_click=Func(self.select_block, i)  # Виклик функції при виборі
            )
            self.hotbar_slots.append(slot)

        # Змінна для вибраного блоку
        self.selected_block_index = 0

    # Функція для вибору блоку
    def select_block(self, index):
        self.selected_block_index = index
        print(f"Selected block: {self.blocks[index]['name']}")