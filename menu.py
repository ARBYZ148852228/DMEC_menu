from tkinter import *

MENU_OPTIONS = ['Возобновить игру', 'Новая игра', 'Сохранить', 'Загрузить', 'Выход']
MENU_WIDTH = 300
MENU_HEIGHT = 200

class MenuHandler:
    def __init__(self, game):
        self.game = game
        self.menu_canvas = None
        self.menu_active = False
        self.current_index = 0

    def toggle_menu(self):
        if self.menu_active:
            self.hide_menu()
        else:
            self.show_menu()

    def show_menu(self):
        if not self.menu_canvas:
            self.menu_canvas = Canvas(self.game.canvas, width=MENU_WIDTH, height=MENU_HEIGHT, bg='grey')
            self.menu_canvas.place(x=(self.game.canvas.winfo_width() - MENU_WIDTH) // 2, y=(self.game.canvas.winfo_height() - MENU_HEIGHT) // 2)
            self.update_menu()
            self.game.window.bind('<KeyPress>', self.navigate_menu)
        self.menu_active = True

    def hide_menu(self):
        if self.menu_canvas:
            self.menu_canvas.destroy()
            self.menu_canvas = None
        self.game.window.unbind('<KeyPress>')
        self.menu_active = False

    def update_menu(self):
        self.menu_canvas.delete('all')
        for index, option in enumerate(MENU_OPTIONS):
            color = 'red' if index == self.current_index else 'black'
            self.menu_canvas.create_text(MENU_WIDTH // 2, 30 * (index + 1), text=option, fill=color, font=('Arial', 16))

    def navigate_menu(self, event):
        if event.keysym == 'Up':
            self.current_index = (self.current_index - 1) % len(MENU_OPTIONS)
            self.update_menu()
        elif event.keysym == 'Down':
            self.current_index = (self.current_index + 1) % len(MENU_OPTIONS)
            self.update_menu()
        elif event.keysym == 'Return':
            self.select_option()

    def select_option(self):
        option = MENU_OPTIONS[self.current_index]
        if option == 'Выход':
            self.game.window.destroy()
        elif option == 'Новая игра':
            self.game.new_game()
        elif option == 'Сохранить':
            self.game.save_game()
        elif option == 'Загрузить':
            self.game.load_game()
        elif option == 'Возобновить игру':
            self.hide_menu()

        self.hide_menu()
