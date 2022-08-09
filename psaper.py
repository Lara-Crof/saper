
from asyncio import events
from curses import window
from tkinter.messagebox import showinfo, showerror
from random import shuffle
import tkinter as tk
from tkinter import Grid, Menu



colors = {
    0: 'white',
    1: 'blue',
    2: 'green',
    3: '#732f2b',
    4: 'red',
    5: 'orange',
    6: 'violet',
    7: 'purple',
    8: 'brown',
}


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, *args, **
                                       kwargs, width=3, font=('Arial', 15, 'bold'))
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton {self.x} {self.y} {self.number} {self.is_mine}'


class Minesweeper:
    win = tk.Tk()
    ROWS = 10
    COLUMNS = 7
    MINES = 10
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):

        self.buttons = []

        for i in range(Minesweeper.ROWS + 2):
            temp = []
            for j in range(Minesweeper.COLUMNS + 2):
                btn = MyButton(Minesweeper.win, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('Button-3', self.right_click )
                temp.append(btn)
            self.buttons.append(temp)

            self.buttons.append(temp)
    
    def right_click(self, event):
        if Minesweeper.IS_GAME_OVER:
            return
        cur_btn = event.widget
        if cur_btn['start'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
            cur_btn['disabledforeground'] = 'red'
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state']= 'normal'
    def click(self, clicked_button: MyButton):

        if Minesweeper.IS_GAME_OVER:
            return

        if Minesweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_buttons()
            Minesweeper.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text='*', bg='red',
                                  disabledforeground='black')
            clicked_button.is_open = True
            Minesweeper.IS_GAME_OVER = True
            showinfo('Game over', 'Вы проиграли!')
            for i in range(1, Minesweeper.ROWS + 1):
                for j in range(1, Minesweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'

        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(
                    text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state=tk.DISABLED)
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):

        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb,
                               disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state=tk.DISABLED)
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        #if not (dx - dy) == 1:
                        #    continue

                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= Minesweeper.ROWS\
                                and 1 <= next_btn.y <= Minesweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def reload(self):
        [child.destroy() for child in  self.win.winfo_children()]
        self.__init__()
        self.create_widgets()
        Minesweeper.IS_FIRST_CLICK = False

    def create_set_win(self):
        win_settings = tk.Toplevel(self.win)
        win_settings.wm_title('Settings')
        tk.Label(win_settings, text=' Коллличество строк').grid(row=0, column=0)
        row_enpty = tk.Entry(win_settings) 
        row_enpty.insert(0, Minesweeper.ROW)
        row_enpty.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_settings, text=' Коллличество колонок').grid(
            row=1, column=0)
        col_enpty = tk.Entry(win_settings)
        col_enpty.insert(0, Minesweeper.COLUMNS)
        col_enpty.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text=' Коллличество бомб').grid(
            row=2, column=0)
        mines_enpty = tk.Entry(win_settings)
        mines_enpty.insert(0, Minesweeper.MINES)
        mines_enpty.grid(row=2, column=1, padx=20, pady=20)
        save_btn = tk.Button(win_settings, text = 'Применить', command= lambda :self.change_setting(row_enpty, col_enpty, mines_enpty))
        save_btn.grid(row=3, column=0, columnspan=2,  padx=20, pady=20)
    
    def change_settings(self, row:tk.Entry, collum: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Mistake', 'вы ввели неправильное значение!')
            return
        Minesweeper.ROWS = int(row.get())
        Minesweeper.COLUMNS = int(collum.get())
        Minesweeper.MINES = int(mines.get())
        self.reload


    def create_widgets(self):

        menubar = tk.Menu(self.win)
        self.win.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoffcommand=0)
        settings_menu.add_command(label='Play', command=self.reload)
        settings_menu.add_command(label='Setting', command = self.create_set_win)
        settings_menu.add_command(label='Exit')
        menubar.add_cascade(label='Fail', menu=settings_menu)
        

    
        count = 1
        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='NWES')
                count += 1
        
        for i in range(1, Minesweeper.ROWS + 1):
            tk.Grid.rowconfigure(self.win, i, weight=1 )
        
        for i in range(1, Minesweeper.COLUMNS + 1):
            tk.Grid.columnconfigure(self.win, i, weight=1)

    def open_all_buttons(self):
        for i in range(Minesweeper.ROWS + 2):
            for j in range(Minesweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', bg='red', disabledforeground='black')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        """Активируем методы"""
        self.create_widgets()

        # self.open_all_buttons()
        Minesweeper.win.mainloop()

    def print_buttons(self):
        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end='')
                else:
                    print(btn.count_bomb, end='')
            print()

    def insert_mines(self, number: int):

        index_mines = self.get_mines_places(number)
        print(index_mines)

        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines_in_buttons(self):
        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomd = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomd += 1
                btn.count_bomb = count_bomd

    @staticmethod
    def get_mines_places(exclude_number: int):

        indexes = list(range(1, Minesweeper.COLUMNS * Minesweeper.ROWS + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:Minesweeper.MINES]


game = Minesweeper()
game.start()
