import tkinter as tk
from tkinter.messagebox import showinfo, askyesno

# Настройки игры
WIDTH = 800
HEIGHT = 600
FPS = 60
PLAYER_SIZE = 100
FINISH_LINE_X = WIDTH - 50
SPEED = 10

# Константы для клавиш
KEY_UP = 'w'
KEY_DOWN = 's'
KEY_ESC = 'Escape'
KEY_ENTER = 'Return'
KEY_PLAYER1 = 'Right'
KEY_PLAYER2 = 'd'
KEY_PAUSE = 'space'

# Опции меню
MENU_OPTIONS = ["Возврат в игру", "Новая игра", "Сохранить", "Загрузить", "Выход"]

# Цвета
BLACK = '#000000'
WHITE = '#FFFFFF'
RED = '#FF0000'
BLUE = '#0000FF'
GREEN = '#00FF00'

# Начальная позиция игроков
x1, y1 = 50, HEIGHT // 2 - PLAYER_SIZE // 2
x2, y2 = 150, HEIGHT // 2 - PLAYER_SIZE // 2

# Переменные состояния игры
menu_mode = True
menu_current_index = 0
game_over = False
pause = False

root = tk.Tk()
root.title('Игровая Приложение')
root.geometry(f'{WIDTH}x{HEIGHT}')
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
canvas.pack(fill=tk.BOTH, expand=True)

player1_rect = canvas.create_rectangle(x1, y1, x1 + PLAYER_SIZE, y1 + PLAYER_SIZE, fill='red', outline='')
player2_rect = canvas.create_rectangle(x2, y2, x2 + PLAYER_SIZE, y2 + PLAYER_SIZE, fill='blue', outline='')

status_text = None


def set_status(text, color=WHITE):
    """Отображение статуса"""
    global status_text
    if status_text is not None:
        canvas.delete(status_text)

    if text != '':
        status_text = canvas.create_text(WIDTH // 2, HEIGHT // 2, text=text, fill=color, font=('Arial', 20))


def pause_toggle():
    """Переключатель паузы"""
    global pause
    if not game_over:
        pause = not pause
        if pause:
            set_status("Игра приостановлена", GREEN)
        else:
            set_status("")


def menu_toggle():
    """Включает/отключает режим меню"""
    global menu_mode
    menu_mode = not menu_mode
    if menu_mode:
        set_status("Меню", WHITE)
    else:
        set_status("")


def key_handler(event):
    """Обработчик нажатий клавиш"""
    global menu_mode, menu_current_index, x1, y1, x2, y2, game_over, pause

    key = event.keysym.lower()

    if menu_mode:
        if key == KEY_UP:
            menu_current_index -= 1
            if menu_current_index < 0:
                menu_current_index = len(MENU_OPTIONS) - 1
        elif key == KEY_DOWN:
            menu_current_index += 1
            if menu_current_index >= len(MENU_OPTIONS):
                menu_current_index = 0
        elif key == KEY_ENTER:
            menu_enter(menu_current_index)
        elif key == KEY_ESC:
            menu_toggle()
    else:
        if key == KEY_PAUSE:
            pause_toggle()
        elif key == KEY_PLAYER1 and not pause and not game_over:
            x1 += SPEED
            canvas.move(player1_rect, SPEED, 0)
        elif key == KEY_PLAYER2 and not pause and not game_over:
            x2 += SPEED
            canvas.move(player2_rect, SPEED, 0)

    check_finish()


def check_finish():
    """Проверка достижения финиша"""
    global game_over
    if x1 >= FINISH_LINE_X or x2 >= FINISH_LINE_X:
        game_over = True
        if x1 > x2:
            set_status("Победил первый игрок!", RED)
        else:
            set_status("Победил второй игрок!", BLUE)


def menu_enter(index):
    """Действия по выбору пунктов меню"""
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
    """Начало новой игры"""
    global x1, y1, x2, y2, game_over, pause
    x1, y1 = 50, HEIGHT // 2 - PLAYER_SIZE // 2
    x2, y2 = 150, HEIGHT // 2 - PLAYER_SIZE // 2
    game_over = False
    pause = False
    set_status("")
    canvas.coords(player1_rect, x1, y1, x1 + PLAYER_SIZE, y1 + PLAYER_SIZE)
canvas.coords(player2_rect, x2, y2, x2 + PLAYER_SIZE, y2 + PLAYER_SIZE)


def game_resume():
    """Возвращение к игре после паузы или меню"""
    global menu_mode
    menu_mode = False
    set_status("")


def game_save():
    pass


def game_load():
    pass


def game_exit():
    if askyesno("Выход", "Вы уверены, что хотите выйти?"):
        root.destroy()


def game_loop():
    root.update()
    root.after(int(1000 / FPS), game_loop)


root.bind_all('<KeyPress>', key_handler)
root.after_idle(game_loop)
root.mainloop()
