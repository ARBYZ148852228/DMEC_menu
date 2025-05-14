from tkinter import *
from pickle import load, dump
from menu import MenuHandler

# Область переменных
GAME_WIDTH = 800
GAME_HEIGHT = 800
PLAYER_SIZE = 100
SPEED = 12

# Координаты игроков
x1, y1 = 50, 50
x2, y2 = x1, y1 + PLAYER_SIZE + 100

# Цвета игроков
PLAYER1_COLOR = 'red'
PLAYER2_COLOR = 'blue'

# Финишная линия
X_FINISH = GAME_WIDTH - 50

# Статусы
game_over = False
pause = False

# Файл сохранения
SAVE_FILE = 'game_save.dat'

class Game:
    def __init__(self, window):
        self.window = window
        self.canvas = Canvas(window, width=GAME_WIDTH, height=GAME_HEIGHT, bg='white')
        self.canvas.pack()
        self.menu = MenuHandler(self)
        self.winner_text = None

        # Создание объектов игры
        self.player1 = self.canvas.create_rectangle(x1, y1, x1 + PLAYER_SIZE, y1 + PLAYER_SIZE, fill=PLAYER1_COLOR)
        self.player2 = self.canvas.create_rectangle(x2, y2, x2 + PLAYER_SIZE, y2 + PLAYER_SIZE, fill=PLAYER2_COLOR)
        self.finish_line = self.canvas.create_rectangle(X_FINISH, 0, X_FINISH + 10, GAME_HEIGHT, fill='black')

        # Привязка клавиш
        self.window.bind('<KeyRelease>', self.key_handler)

    def key_handler(self, event):
        global x1, x2, pause
        if not game_over:
            if event.keysym == 'd':
                x1 += SPEED
            elif event.keysym == 'Right':
                x2 += SPEED
            elif event.keysym == 'Escape':
                self.menu.toggle_menu()
            elif event.keysym == 'p':
                pause = not pause

        self.check_finish()
        self.update_players()

    def check_finish(self):
        global game_over
        if not game_over:
            if x1 + PLAYER_SIZE >= X_FINISH:
                self.display_winner("Красный игрок победил!", PLAYER1_COLOR)
                game_over = True
            elif x2 + PLAYER_SIZE >= X_FINISH:
                self.display_winner("Синий игрок победил!", PLAYER2_COLOR)
                game_over = True

    def display_winner(self, message, color):
        self.winner_text = self.canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, text=message, fill=color, font=('Arial', 30))

    def update_players(self):
        self.canvas.coords(self.player1, x1, y1, x1 + PLAYER_SIZE, y1 + PLAYER_SIZE)
        self.canvas.coords(self.player2, x2, y2, x2 + PLAYER_SIZE, y2 + PLAYER_SIZE)

    def save_game(self):
        with open(SAVE_FILE, 'wb') as f:
            dump((x1, y1, x2, y2), f)
        print("Игра сохранена")

    def load_game(self):
        global x1, y1, x2, y2
        try:
            with open(SAVE_FILE, 'rb') as f:
                x1, y1, x2, y2 = load(f)
            print("Игра загружена")
        except FileNotFoundError:
            print("Файл сохранения не найден")
        self.update_players()

    def new_game(self):
        global x1, y1, x2, y2, game_over
        x1, y1 = 50, 50
        x2, y2 = x1, y1 + PLAYER_SIZE + 100
        game_over = False
        if self.winner_text:
            self.canvas.delete(self.winner_text)
        print("Новая игра начата")
        self.update_players()

    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    root = Tk()
    root.title("Догони меня, если сможешь")
    game = Game(root)
    game.start()
