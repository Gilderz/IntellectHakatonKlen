from ursina import *

class Menu:
    def __init__(self):
        self.menu_active = False

        # Створення меню
        self.menu = Entity(
            parent=camera.ui,  # Прив'язка до інтерфейсу камери
            model='quad',  # Модель для фону меню
            scale=(0.6, 0.4),  # Розмір меню
            color=color.dark_gray,  # Колір фону
            enabled=False  # Спочатку меню вимкнене
        )

        # Кнопка "Нова гра"
        self.new_game_button = Button(
            parent=self.menu,
            text="Нова гра",
            color=color.azure,
            scale=(0.8, 0.1),
            y=0.05,  # Позиція по вертикалі
            on_click=self.start_new_game  # Дія при натисканні
        )

        # Кнопка "Вихід"
        self.quit_button = Button(
            parent=self.menu,
            text="Вихід",
            color=color.red,
            scale=(0.8, 0.1),
            y=-0.15,  # Позиція по вертикалі
            on_click=self.quit_game  # Дія при натисканні
        )

    # Функція для початку нової гри
    def start_new_game(self):
        self.menu.enabled = False  # Приховуємо меню
        self.menu_active = False
        return True  # Повертаємо управління гравцем

    # Функція для виходу з гри
    def quit_game(self):
        quit()

    # Функція для перемикання стану меню
    def toggle_menu(self):
        self.menu_active = not self.menu_active
        self.menu.enabled = self.menu_active
        return not self.menu_active  # Повертаємо стан управління гравцем