from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

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

# Змінна для відстеження стану меню
menu_active = False

# Створення меню
menu = Entity(
    parent=camera.ui,  # Прив'язка до інтерфейсу камери
    model='quad',  # Модель для фону меню
    scale=(0.6, 0.4),  # Розмір меню
    color=color.dark_gray,  # Колір фону
    enabled=False  # Спочатку меню вимкнене
)

# Кнопка "Нова гра"
new_game_button = Button(
    parent=menu,
    text="Нова гра",
    color=color.azure,
    scale=(0.8, 0.1),
    y=0.05,  # Позиція по вертикалі
    on_click=lambda: start_new_game()  # Дія при натисканні
)

# Кнопка "Вихід"
quit_button = Button(
    parent=menu,
    text="Вихід",
    color=color.red,
    scale=(0.8, 0.1),
    y=-0.15,  # Позиція по вертикалі
    on_click=lambda: quit()  # Дія при натисканні
)

# Функція для початку нової гри
def start_new_game():
    global menu_active
    menu.enabled = False  # Приховуємо меню
    menu_active = False
    player.enabled = True  # Повертаємо управління гравцем

# Функція для вибору блоку
def select_block(index):
    global selected_block_index
    selected_block_index = index
    print(f"Selected block: {blocks[index]['name']}")

# Хотбар
hotbar = Entity(
    parent=camera.ui,
    model='quad',
    scale=(0.6, 0.1),
    y=-0.45,  # Позиція внизу екрану
    color=color.gray
)

# Блоки для хотбару
blocks = [
    {"color": color.red, "name": "Red Block"},
    {"color": color.blue, "name": "Blue Block"},
    {"color": color.yellow, "name": "Yellow Block"}
]

# Відображення блоків у хотбарі
hotbar_slots = []
for i, block in enumerate(blocks):
    slot = Button(
        parent=hotbar,
        model='cube',
        color=block["color"],
        scale=(0.1, 0.1),
        x=-0.25 + i * 0.25,  # Розташування слотів
        text=str(i + 1),  # Відображення цифри для вибору
        on_click=Func(select_block, i)  # Виклик функції при виборі
    )
    hotbar_slots.append(slot)

# Змінна для вибраного блоку
selected_block_index = 0

# Функція для розміщення блоку
def place_block():
    if mouse.hovered_entity:  # Якщо курсор наведений на об'єкт
        position = mouse.hovered_entity.position + mouse.normal  # Позиція для нового блоку
        Entity(
            model='cube',
            color=blocks[selected_block_index]["color"],
            position=position,
            texture="white_cube",
            parent=ground,  # Додаємо новий блок до батьківського об'єкта
            collider='box'  # Додаємо колайдер для взаємодії
        )

# Функція для знищення блоку
def destroy_block():
    if mouse.hovered_entity and mouse.hovered_entity != ground:  # Якщо курсор наведений на блок
        destroy(mouse.hovered_entity)  # Видаляємо блок

# Інвентар
inventory = Entity(
    parent=camera.ui,
    model='quad',
    scale=(0.6, 0.6),
    color=color.dark_gray,
    enabled=False  # Спочатку інвентар прихований
)

# Створення сітки інвентаря (9x9 комірок)
inventory_grid = []
cell_size = 16  # Розмір комірки в пікселях
for y in range(9):
    for x in range(9):
        cell = Entity(
            parent=inventory,
            model='quad',
            color=color.white,
            scale=(cell_size / window.size[0], cell_size / window.size[1]),
            x=-0.4 + x * 0.1,
            y=0.4 - y * 0.1,
            alpha=0.5  # Прозорість комірки
        )
        inventory_grid.append(cell)

# Функція для відкриття/закриття інвентаря
def toggle_inventory():
    inventory.enabled = not inventory.enabled
    player.enabled = not inventory.enabled  # Блокуємо або розблоковуємо управління гравцем

# Обробка введення
def input(key):
    global shift_click, normal_speed, menu_active

    if key == 'tab':
        menu_active = not menu_active  # Перемикаємо стан меню
        menu.enabled = menu_active  # Показуємо або приховуємо меню
        player.enabled = not menu_active  # Блокуємо або розблоковуємо управління гравцем

    if key == 'shift' and not menu_active:
        if shift_click % 2 == 0:
            player.speed = normal_speed + 3
        else:
            player.speed = normal_speed
        shift_click += 1

    # Вибір блоку за допомогою цифрових клавіш
    if key in ('1', '2', '3'):
        select_block(int(key) - 1)

    # Розміщення блоку лівою кнопкою миші
    if key == 'left mouse down' and not menu_active:
        place_block()

    # Знищення блоку правою кнопкою миші
    if key == 'right mouse down' and not menu_active:
        destroy_block()

    # Відкриття/закриття інвентаря
    if key == 'e':
        toggle_inventory()

# Запуск додатку
app.run()