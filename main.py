from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from hotbar import Hotbar  # Імпортуємо клас Hotbar
from menu import Menu  # Імпортуємо клас Menu
from inventory import Inventory  # Імпортуємо клас Inventory

app = Ursina()

# Налаштування вікна
window.size = (1152, 720)
window.icon = 'textures/ursina.ico'  # Додайте іконку, якщо потрібно

# Створення сітки кубів
ground = Entity(model=None, collider=None)  # Батьківський об'єкт для всіх блоків
for x in range(16):
    for z in range(16):
        block = Entity(
            model='cube',
            texture='white_cube',
            position=Vec3(x, 0, z),
            parent=ground,  # Додаємо блок до батьківського об'єкта
            collider='box'  # Додаємо колайдер для взаємодії
        )

# Ініціалізація першого особистого контролера
player = FirstPersonController()

# Вимкнення гравітації
player.gravity = 0.0

# Глобальні змінні для контролю швидкості
shift_click = 0
normal_speed = player.speed

# Ініціалізація хотбару
hotbar = Hotbar()

# Ініціалізація меню
menu = Menu()

# Ініціалізація інвентаря
inventory = Inventory()

# Функція для розміщення блоку
def place_block():
    if mouse.hovered_entity:  # Якщо курсор наведений на об'єкт
        position = mouse.hovered_entity.position + mouse.normal  # Позиція для нового блоку
        Entity(
            model='cube',
            color=hotbar.blocks[hotbar.selected_block_index]["color"],
            position=position,
            texture="white_cube",
            parent=ground,  # Додаємо новий блок до батьківського об'єкта
            collider='box'  # Додаємо колайдер для взаємодії
        )

# Функція для знищення блоку
def destroy_block():
    if mouse.hovered_entity and mouse.hovered_entity != ground:  # Якщо курсор наведений на блок
        destroyed_block = mouse.hovered_entity
        destroy(destroyed_block)  # Видаляємо блок
        inventory.add_item(destroyed_block)  # Додаємо блок до інвентаря

# Обробка введення
def input(key):
    global shift_click, normal_speed

    if key == 'esc':
        player.enabled = menu.toggle_menu()  # Перемикаємо меню та управління гравцем

    if key == 'shift' and not menu.menu_active:
        if shift_click % 2 == 0:
            player.speed = normal_speed + 3
        else:
            player.speed = normal_speed
        shift_click += 1

    # Вибір блоку за допомогою цифрових клавіш
    if key in ('1', '2', '3'):
        hotbar.select_block(int(key) - 1)

    # Розміщення блоку лівою кнопкою миші
    if key == 'left mouse down' and not menu.menu_active:
        place_block()

    # Знищення блоку правою кнопкою миші
    if key == 'right mouse down' and not menu.menu_active:
        destroy_block()

    # Відкриття/закриття інвентаря
    if key == 'e':
        player.enabled = inventory.toggle_inventory()

# Запуск додатку
app.run()