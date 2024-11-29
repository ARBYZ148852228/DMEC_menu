import pygame
from sys import exit

# Настройки игры
WIDTH = 800
HEIGHT = 600
FPS = 60
PLAYER_SIZE = 100
FINISH_LINE_X = WIDTH - 50
SPEED = 10

# Константы для клавиш
KEY_UP = pygame.K_w
KEY_DOWN = pygame.K_s
KEY_ESC = pygame.K_ESCAPE
KEY_ENTER = pygame.K_RETURN
KEY_PLAYER1 = pygame.K_RIGHT
KEY_PLAYER2 = pygame.K_d
KEY_PAUSE = pygame.K_SPACE

# Опции меню
MENU_OPTIONS = ["Возврат в игру", "Новая игра", "Сохранить", "Загрузить", "Выход"]

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Начальная позиция игроков
x1, y1 = 50, HEIGHT // 2 - PLAYER_SIZE // 2
x2, y2 = 150, HEIGHT // 2 - PLAYER_SIZE // 2

# Переменные состояния игры
menu_mode = True
menu_current_index = 0
game_over = False
pause = False


def set_status(text, color=WHITE):
    """Отображает статусное сообщение"""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface,
                (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - text_surface.get_height() // 2))


def pause_toggle():
    """Переключение паузы"""
    global pause
    if not game_over:
        pause = not pause
        if pause:
            set_status("Игра приостановлена", GREEN)
        else:
            set_status("", BLACK)


def menu_toggle():
    """Включение/выключение режима меню"""
    global menu_mode
    menu_mode = not menu_mode
    if menu_mode:
        set_status("Меню", WHITE)
    else:
        set_status("", BLACK)


def key_handler(event):
    """Обработка событий клавиатуры"""
    global menu_mode, menu_current_index, x1, y1, x2, y2, game_over, pause

    # Обрабатываем события клавиатуры
    if event.type == pygame.KEYDOWN:
        if event.key == KEY_UP:
            menu_current_index -= 1
            if menu_current_index < 0:
                menu_current_index = len(MENU_OPTIONS) - 1
        elif event.key == KEY_DOWN:
            menu_current_index += 1
            if menu_current_index >= len(MENU_OPTIONS):
                menu_current_index = 0
        elif event.key == KEY_ENTER:
            menu_enter(menu_current_index)
        elif event.key == KEY_ESC:
            menu_toggle()
        elif event.key == KEY_PAUSE:
            pause_toggle()
        elif event.key == KEY_PLAYER1 and not pause and not game_over:
            x1 += SPEED
        elif event.key == KEY_PLAYER2 and not pause and not game_over:
            x2 += SPEED


def check_finish():
    """Проверяем, достиг ли кто-то финишной черты"""
    global game_over
    if x1 >= FINISH_LINE_X or x2 >= FINISH_LINE_X:
        game_over = True
        if x1 > x2:
            set_status("Победил первый игрок!", RED)
        else:
            set_status("Победил второй игрок!", BLUE)


def menu_enter(index):
    """Выполнение действий, связанных с выбором пункта меню"""
    global menu_mode, x1, y1, x2, y2, game_over, pause
    if index == 0:  # Возврат в игру
        menu_mode = False
    elif index == 1:  # Новая игра
        game_new()
    elif index == 2:  # Сохранить
        game_save()
    elif index == 3:  # Загрузить
        game_load()
    elif index == 4:  # Выход
        game_exit()


def game_new():
    """Начинает новую игру"""
    global x1, y1, x2, y2, game_over, pause
    x1, y1 = 50, HEIGHT // 2 - PLAYER_SIZE // 2
    x2, y2 = 150, HEIGHT // 2 - PLAYER_SIZE // 2
    game_over = False
    pause = False
    set_status("", BLACK)


def game_resume():
    """Возвращаемся к игре после паузы или меню"""
    global menu_mode
    menu_mode = False
    set_status("", BLACK)


def game_save():