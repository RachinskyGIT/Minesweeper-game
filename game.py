import tkinter as tk
import random
import os
base_dir = os.path.dirname(__file__)

class MinesweeperGUI:
    def __init__(self, master, size="small", dificulty="easy"):
        self.master = master
        self.master.config(bg="khaki")
        self.size = size
        self.row_col_generation()
        self.dificulty = dificulty
        self.mines = self.amount_of_mines()
        self.photos = self.images(*self.random_image_numbers())
        self.grid = [[0 for c in range(self.cols)] for r in range(self.rows)]
        self.cells = [[None for c in range(self.cols)] for r in range(self.rows)]
        self.visible = [[False for c in range(self.cols)] for r in range(self.rows)]
        self.count_visible = 0
        self.time_elapsed = 0
        self.generate_mines()
        self.update_grid()
        self.create_widgets()
        self.fail = False
    

        #"change oops face when clicking"-set
        for r in range(self.rows):
            for c in range(self.cols):
                button = self.cells[r][c]
                button.bind('<Button-1>', lambda event, row=r, col=c: self.on_left_click(row, col, event))
                button.bind("<ButtonRelease-1>", lambda event, row=r, col=c: self.on_button_release(row, col, event))

    def row_col_generation(self):
        if self.size == "small":
            self.rows, self.cols = 10, 10
        elif self.size == "medium":
            self.rows, self.cols = 15, 15
        else:
            self.rows, self.cols = 20, 20

    #function for setting oops face when stepping to cell
    def on_left_click(self, row, col, event):
        if self.cells[row][col].cget('state') != 'disabled':
            if not self.winning() or self.fail:
                self.oops_img = tk.PhotoImage(file = rf"{base_dir}\pics\oops{random.randint(1, 5)}.png").subsample(2)
                self.reset_button.config(image=self.oops_img)

        # self.current_cell = (self.reveal_cell(row, col))
                

    #function for setting regular face when un-stepping from cell
    def on_button_release(self, row, col, event):
        if not (self.winning() or self.fail):

            #This command puts a normal muzzle only after 0.3 seconds of showing the oops muzzle. 
            # Therefore, victory and defeat faces are placed only 0.3001 seconds after the 
            # victory or defeat itself, in order to be placed after the oops face, and not before.
            root.after(300, lambda: self.reset_button.config(image=self.photos['reg']))
            # self.reset_button.config(image=self.photos['reg'])
    
    #that function makes random image numbers every new game
    def random_image_numbers(self):
        rand_num_reg = random.randint(1, 4)
        rand_num_die = random.randint(1, 5)
        rand_num_win = random.randint(1, 2)
        return [rand_num_reg, rand_num_die, rand_num_win]

    #function that chooses which files will be smiley faces images
    def images(self, rand_num_reg, rand_num_die, rand_num_win):
        reg = tk.PhotoImage(file = rf"{base_dir}\pics\reg{rand_num_reg}.png").subsample(2)
        die = tk.PhotoImage(file = rf"{base_dir}\pics\die{rand_num_die}.png").subsample(2)
        win = tk.PhotoImage(file = rf"{base_dir}\pics\win{rand_num_win}.png").subsample(2)
        pics = {'reg':reg, 'die': die, 'win': win}
        return pics
    
    # #cells pictures - didn't realized yet
    # def cell_pics (self):     
    #     cell_0 = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_{0}.png")
    #     cell_1 = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_{1}.png")
    #     cell_2 = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_{2}.png")
    #     cell_3 = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_{3}.png")
    #     cell_4 = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_{4}.png")
    #     cell_5 = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_{5}.png")
    #     cell_6 = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_{6}.png")
    #     cell_7 = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_{7}.png")
    #     cell_8 = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_{8}.png")
    #     cell_unrevealed = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_unrevealed.png")
    #     cell_flag = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_flag.png")
    #     cell_question = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_question.png")
    #     cell_mine = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_mine.png")
    #     cell_redmine = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_redmine.png")
    #     cell_crossedmine = tk.PhotoImage(file = rf"{base_dir}\240x240\cell_crossedmine.png")
    #     cells = {'cell_0':cell_0, 'cell_1':cell_1, 'cell_2':cell_2, 'cell_3':cell_3, 'cell_4':cell_4, 'cell_5':cell_5,\
    #             'cell_6':cell_6, 'cell_7':cell_7, 'cell_8':cell_8, 'cell_unrevealed':cell_unrevealed,\
    #                  'cell_flag':cell_flag, 'cell_question':cell_question, 'cell_mine':cell_mine,\
    #                         'cell_redmine':cell_redmine, 'cell_crossedmine':cell_crossedmine}
    #     return cells


    #choosing game difficulty
    def amount_of_mines(self):
        if self.dificulty == "easy":
            return int(self.cols*self.rows*0.1)
        if self.dificulty == "medium":
            return int(self.cols*self.rows*0.2)
        if self.dificulty == "hard":
            return int(self.cols*self.rows*0.3)
        if self.dificulty == "hell":
            return int(self.cols*self.rows*0.6)
        if self.dificulty == "pure luck":
            return int(self.cols*self.rows*0.95)

    def generate_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.grid[row][col] != -1:
                self.grid[row][col] = -1
                mines_placed += 1

    def update_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != -1:
                    self.grid[row][col] = self.count_adjacent_mines(row, col)

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r >= 0 and r < self.rows and c >= 0 and c < self.cols and self.grid[r][c] == -1:
                    count += 1
        return count

    def update_mine_counter(self):
        self.mine_counter_label.config(text=f"{self.mines_remaining:03}")


    def create_widgets(self):
        # create menu bar
        self.menu_bar = tk.Menu(self.master, bg="khaki")

        # create dificulty dropdown widget
        self.widget_dificulty()

        # create size dropdown
        self.widget_size()

        # create the menu frame
        self.menu = tk.Frame(self.master, bg="khaki")
        self.menu.pack(pady=5)

        # create frame to contain the cells
        self.frame = tk.Frame(self.master, bg="khaki")
        self.frame.pack(pady=5)

        # create cells
        self.widget_cells()

        # create mine counter label
        self.widget_mine_counter()
        
        # create reset button
        self.widget_reset_button()

        # create timer
        self.widget_timer()

        self.master.config(menu=self.menu_bar)

    def delete_widgets(self):
        self.menu.destroy()
        self.frame.destroy()


    def widget_size(self):
        size_menu = tk.Menu(self.menu_bar, tearoff=0)
        sizes = ["small", "medium", "big"]
        for size in sizes:
            size_menu.add_command(label=size, command=lambda s=size: self.size_button(s))

        self.menu_bar.add_cascade(label="Size", menu=size_menu)

    def size_button(self, size):
        self.size = size
        self.reset_board()

    def widget_dificulty(self):
        dificulty_menu = tk.Menu(self.menu_bar, tearoff=0)
        dificulties = ["easy", "medium", "hard", "hell", "pure luck"]
        for dificulty in dificulties:
            dificulty_menu.add_command(label=dificulty, command=lambda d=dificulty: self.dificulty_button(d))

        self.menu_bar.add_cascade(label="Dificulty", menu=dificulty_menu)
    
    def dificulty_button(self, dificulty):
        self.dificulty = dificulty
        self.reset_game()


    def widget_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                # create a cell button
                cell = tk.Button(self.frame, width=2, height=1, bg="grey", command=lambda r=row, c=col: self.reveal_cell(r, c))
                cell.bind("<Button-3>", lambda event, r=row, c=col: self.unflag_mine(r, c))
                cell.grid(row=row, column=col)

                # add the button to the list of cells
                self.cells[row][col] = cell
                #colorize cells
                self.widget_colorize_cell(row, col)
   

    def widget_colorize_cell(self, row, col):
        cell = self.cells[row][col]
        if self.grid[row][col] in range(-1,9):
            cell.config(font="bold")
        if self.grid[row][col] == 0:
            cell.config(fg='light grey', activeforeground=cell["bg"],disabledforeground='light grey') #makes zeroes to be invisible
        if self.grid[row][col] == 1:
            cell.config(fg='blue', disabledforeground='blue')        
        if self.grid[row][col] == 2:
            cell.config(fg='green', disabledforeground='green')
        if self.grid[row][col] == 3:
            cell.config(fg='red', disabledforeground='red')         
        if self.grid[row][col] == 4:
            cell.config(fg='dark blue', disabledforeground='dark blue')
        if self.grid[row][col] == 5:
            cell.config(fg='dark red', disabledforeground='dark red')
        if self.grid[row][col] == 6:
            cell.config(fg='cyan', disabledforeground='cyan')
        if self.grid[row][col] == 7:
            cell.config(fg='brown', disabledforeground='brown')
        if self.grid[row][col] == 8:
            cell.config(fg='black', disabledforeground='black')                     


    def widget_mine_counter(self):
        self.mines_remaining = self.mines
        self.mine_counter_label = tk.Label(
            self.menu, text=f"{self.mines_remaining:03}",
            font=("Arial", 20), bg="black", fg="red", width=8, height=1
        )
        self.mine_counter_label.pack(side=tk.LEFT, padx= 10)

    def widget_reset_button(self):
        self.reset_button = tk.Button(self.menu, text='Reset', image = self.photos['reg'], command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def widget_timer(self):
        self.timer_label = tk.Label(
            self.menu, text=f"Time: {self.time_elapsed}", font=("Arial", 20),
            bg="black", fg="red", width=8, height=1
        )
        self.timer_label.pack(side=tk.LEFT, padx= 10)

    def start_timer(self):
        self.timer_label.config(text=f"Time: {self.time_elapsed}")
        self.timer_id = self.master.after(1000, self.start_timer)
        self.time_elapsed += 1


    def winning(self):
        self.count_visible = 0
        # checks if all the revealed cells is non-mines:
        for r in range(self.rows):
            for c in range(self.cols):
                if (self.visible[r][c] == True) and (self.grid[r][c] != -1):
                    self.count_visible +=1
        # if visible cells there are only non-mines cells - victory
        if self.count_visible == (self.rows*self.cols - self.mines):
            self.mine_counter_label.config(text=f"You WON!")
            root.after(301, lambda: self.reset_button.configure(image=self.photos['win']))
            # self.reset_button.configure(image=self.photos['win'])
            for r in range(self.rows):
                for c in range(self.cols):
                    self.cells[r][c].config(state='disabled', fg='black') #blocks cells buttons after win
            self.master.after_cancel(self.timer_id) #stops the timer
            self.count_visible = self.rows*self.cols
            return True
        return False
    

    def defeat(self, r, c):
        self.mine_counter_label.config(text=f"Boom!!") #changes mine counter to "boom" after boom
        root.after(301, lambda: self.reset_button.configure(image=self.photos['die']))
        # self.reset_button.configure(image=self.photos['die'])
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].config(state='disabled', fg='black') #blocks cells buttons after boom
                if self.grid[r][c] == -1: #reveals all other mines
                    self.visible[r][c] = True
        self.master.after_cancel(self.timer_id) #stops the timer
        self.count_visible = self.rows*self.cols 
        self.fail = True


    def reveal_cell(self, row, col):
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()

            if not self.visible[r][c] and self.cells[r][c]["text"] != u"\U000026A0" and self.cells[r][c]["text"] != "?":
                self.visible[r][c] = True
                self.cells[r][c].config(state='disabled', fg='black')

                if self.grid[r][c] == 0:
                    for i, j in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (-1, -1), (1, -1), (1, 1)):
                        nr, nc = r + i, c + j
                        if (0 <= nr < self.rows) and (0 <= nc < self.cols) and not(self.visible[nr][nc]) and not((nr, nc) in stack):
                            stack.append((nr, nc))

                elif self.grid[r][c] == -1:
                    self.defeat(r, c)
        self.current_cell = (row,col)

        self.update_cells()


    def unflag_mine(self, row, col):
        if not self.winning():
            if not self.fail:
                if not self.visible[row][col]: 
                    if self.cells[row][col]["text"] == u"?":
                        # self.widget_colorize_cell(row, col)
                        self.cells[row][col].config(text="", bg="grey")
                        self.update_mine_counter()
                    elif self.cells[row][col]["text"] == u"\U000026A0":
                        # self.widget_colorize_cell(row, col)
                        self.cells[row][col].config(text="?", bg="grey")
                        self.mines_remaining += 1
                        self.update_mine_counter()
                    else:
                        self.cells[row][col].config(text=u"\U000026A0", bg="grey")
                        self.cells[row][col].config(fg='black')
                        self.mines_remaining -= 1
                        self.update_mine_counter()

    #checks after every turn
    def update_cells(self):
        #check after every turn if it is winning
        self.winning()
        #actions with cells after each action
        for row in range(self.rows):
            for col in range(self.cols):
                #what to do if cell is visible
                if self.visible[row][col]:
                    #marking cell when cell is a mine    
                    if self.grid[row][col] == -1:
                        if self.cells[row][col]["text"] == u"\U000026A0":
                            self.cells[row][col].config(text=u"\U000029BB",disabledforeground="black", bg="green",font=("bold"))
                        elif (row == self.current_cell[0]) and (col == self.current_cell[1]):
                            self.cells[row][col].config(text=u"\U00002620",disabledforeground="black", bg="red",font=("bold"))                        
                        else:
                            self.cells[row][col].config(text=u"\U000026EF",disabledforeground="black", bg="red",font=("bold"))
                    #what to do if cell is visible and not a mine
                    else:
                        self.cells[row][col].config(text=str(self.grid[row][col]), bg="light grey", state='disabled')
                #what to do if cell is not visible
                else:
                    #re-colorizing flags every turn
                    if self.cells[row][col]["text"] == u"\U000026A0":
                        self.cells[row][col].config(text=u"\U000026A0", bg="grey", disabledforeground="black")
                    elif self.cells[row][col]["text"] == "?":
                        self.cells[row][col].config(text="?", bg="grey", disabledforeground="black")
                    elif self.grid[row][col] == -1 and self.winning():
                        self.cells[row][col].config(text=u"\U000026A0",disabledforeground="black", bg="grey",font=("bold"))
                    else:
                        self.cells[row][col].config(text="", bg="grey")

    def reset_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.widget_colorize_cell(row, col)
                self.cells[row][col].config(text="", bg="grey")
                self.cells[row][col].config(state='normal')
        self.mines_remaining = self.mines
        self.update_mine_counter()

    def reset_board(self):
        self.row_col_generation()
        self.mines = self.amount_of_mines()
        self.grid = [[0 for c in range(self.cols)] for r in range(self.rows)]
        self.cells = [[None for c in range(self.cols)] for r in range(self.rows)]
        self.visible = [[False for c in range(self.cols)] for r in range(self.rows)]
        self.generate_mines()
        self.update_grid()
        self.delete_widgets()
        self.create_widgets()
        #makes new random smiley faces every game
        self.photos = self.images(*self.random_image_numbers())
        self.reset_button.configure(image=self.photos['reg'])
        self.fail = False

        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

        self.time_elapsed = 0
        self.timer_label.config(text="Time: 0")
        self.start_timer()

    def reset_game(self):
        self.mines = self.amount_of_mines()
        self.grid = [[0 for c in range(self.cols)] for r in range(self.rows)]
        self.visible = [[False for c in range(self.cols)] for r in range(self.rows)]
        self.generate_mines()
        self.update_grid()
        self.reset_cells()
        #makes new random smiley faces every game
        self.photos = self.images(*self.random_image_numbers())
        self.reset_button.configure(image=self.photos['reg'])
        self.fail = False

        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

        self.time_elapsed = 0
        self.timer_label.config(text="Time: 0")
        self.start_timer()

    def play(self):
        self.start_timer()
        self.master.mainloop()






if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = MinesweeperGUI(root)
    game.play()
    