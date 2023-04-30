import tkinter as tk
import random


class MinesweeperGUI:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[0 for c in range(cols)] for r in range(rows)]
        self.visible = [[False for c in range(cols)] for r in range(rows)]
        self.generate_mines()
        self.update_grid()
        self.create_widgets()
        self.time_elapsed = 0
        # self.timer_label = tk.Label(self.master, text="Time: 0")
        self.timer_label = tk.Label(
            self.master, text="Time: 0", font=("Arial", 16),
            bg="black", fg="red", width=8, height=1
        )
        self.timer_label.pack(padx = 1, pady = 0.5, side=tk.RIGHT)
        # self.timer_label.place() #anchor = tk.CENTER

        self.timer_id = None

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
        self.mine_counter_label.config(text=f"Mines: {self.mines_remaining}")




    def create_widgets(self):
        # frame
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        # mine counter
        self.mines_remaining = self.mines
        self.mine_counter_label = tk.Label(
            self.master, text=f"Mines: {self.mines_remaining}", font=("Arial", 16),
            bg="black", fg="red", width=8, height=1
        )
        self.mine_counter_label.pack(padx = 1, pady = 0.5, side=tk.LEFT)
        # self.mine_counter_label.place() #anchor = tk.CENTER
        # self.mine_counter_label.pack(padx = 1, pady = 0.5, side=tk.LEFT)
        # cells 
        self.cells = []
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                cell = tk.Button(self.frame, width=2, height=1, command=lambda r=row, c=col: self.reveal_cell(r, c))
                cell.bind("<Button-3>", lambda event, r=row, c=col: self.unflag_mine(r, c)) # unflag mine method
                cell.grid(row=row, column=col)
                row_cells.append(cell)
            self.cells.append(row_cells)
        # reset button
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT)
        # color counters
        
        # self.timer_label = tk.Label(
        #     self.master, text="000", font=("Arial", 16),
        #     bg="black", fg="red", width=6, height=1
        # )
        # self.timer_label.place(x=self.cols*30-50, y=10)


    def start_timer(self):
        self.timer_label.config(text=f"Time: {self.time_elapsed}")
        self.timer_id = self.master.after(1000, self.start_timer)
        self.timer_id
        self.time_elapsed += 1


    def reveal_cell(self, row, col):
        if not self.visible[row][col] and self.cells[row][col]["text"] != "F":
            self.visible[row][col] = True
            if self.grid[row][col] == 0:
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        if r >= 0 and r < self.rows and c >= 0 and c < self.cols:
                            self.reveal_cell(r, c)
            # flag mine method
            elif self.grid[row][col] == -1:
                # self.cells[row][col].config(text="F", bg="light grey")
                self.mines_remaining -= 1
                self.update_mine_counter()
        self.update_cells()


    def unflag_mine(self, row, col):
        if not self.visible[row][col]: 
            if self.cells[row][col]["text"] == "F":
                self.cells[row][col].config(text="", bg="grey")
                self.mines_remaining += 1
                self.update_mine_counter()
            else:
                self.cells[row][col].config(text="F", bg="grey")
                self.mines_remaining -= 1
                self.update_mine_counter()


    def update_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.visible[row][col]:
                    if self.grid[row][col] == -1:
                        self.cells[row][col].config(text="*", bg="red")
                    else:
                        self.cells[row][col].config(text=str(self.grid[row][col]), bg="light grey")
                else:
                    if self.cells[row][col]["text"] == "F":
                        self.cells[row][col].config(text="F", bg="grey")
                    else:
                        self.cells[row][col].config(text="", bg="grey")

    def reset_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].config(text="", bg="grey")
        self.mines_remaining = self.mines
        self.update_mine_counter()

    def reset_game(self):
        self.grid = [[0 for c in range(self.cols)] for r in range(self.rows)]
        self.visible = [[False for c in range(self.cols)] for r in range(self.rows)]
        self.generate_mines()
        self.update_grid()
        self.reset_cells()

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
    rows = 10
    cols = 10
    mines = 8
    root = tk.Tk()
    root.title("Minesweeper")
    game = MinesweeperGUI(root, rows, cols, mines)
    game.play()
    