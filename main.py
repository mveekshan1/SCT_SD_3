import tkinter as tk
from tkinter import messagebox

# Solver backend functions

def find_empty(grid):

    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return (r, c)
    return None

def is_valid(grid, row, col, val):
    
    # Row check
    if any(grid[row][x] == val for x in range(9)):
        return False
    # Column check
    if any(grid[y][col] == val for y in range(9)):
        return False
    # 3x3 block check
    start_r = row - row % 3
    start_c = col - col % 3
    for r in range(start_r, start_r + 3):
        for c in range(start_c, start_c + 3):
            if grid[r][c] == val:
                return False
    return True

def solve_backtracking(grid):
    
    empty = find_empty(grid)
    if not empty:
        return True  # Puzzle solved
    row, col = empty

    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            if solve_backtracking(grid):
                return True
            grid[row][col] = 0  # backtrack
    return False


# GUI: Tkinter front end

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        root.title("Sudoku Solver — Backtracking (Python + Tkinter)")
        root.resizable(False, False)

        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self._build_grid()
        self._build_controls()
        self._example_grid = [
            [5,3,0, 0,7,0, 0,0,0],
            [6,0,0, 1,9,5, 0,0,0],
            [0,9,8, 0,0,0, 0,6,0],
            [8,0,0, 0,6,0, 0,0,3],
            [4,0,0, 8,0,3, 0,0,1],
            [7,0,0, 0,2,0, 0,0,6],
            [0,6,0, 0,0,0, 2,8,0],
            [0,0,0, 4,1,9, 0,0,5],
            [0,0,0, 0,8,0, 0,7,9]
        ]

    def _build_grid(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.grid(row=0, column=0)
        # Create 9x9 Entry widgets
        for r in range(9):
            for c in range(9):
                e = tk.Entry(frame, width=2, font=('Helvetica', 18), justify='center')
                e.grid(row=r, column=c, padx=(0 if c % 3 else 4, 0), pady=(0 if r % 3 else 4, 0))
                # validate on keypress: allow only digits 1-9 or empty
                e.configure(validate='key', validatecommand=(self.root.register(self._validate_digit), '%P'))
                self.cells[r][c] = e

    def _build_controls(self):
        ctrl = tk.Frame(self.root, pady=10)
        ctrl.grid(row=1, column=0, sticky='ew')

        solve_btn = tk.Button(ctrl, text="Solve", command=self.on_solve, width=10)
        solve_btn.grid(row=0, column=0, padx=5)

        clear_btn = tk.Button(ctrl, text="Clear", command=self.on_clear, width=10)
        clear_btn.grid(row=0, column=1, padx=5)

        load_btn = tk.Button(ctrl, text="Load Example", command=self.load_example, width=12)
        load_btn.grid(row=0, column=2, padx=5)

        print_btn = tk.Button(ctrl, text="Print Grid (console)", command=self.print_grid, width=15)
        print_btn.grid(row=0, column=3, padx=5)

    def _validate_digit(self, P):
       
        if P == "":
            return True
        if len(P) > 1:
            return False
        return P in '123456789'

    def read_grid(self):
        
        grid = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.cells[r][c].get().strip()
                row.append(int(val) if val != "" else 0)
            grid.append(row)
        return grid

    def write_grid(self, grid, original_grid=None):
        
        for r in range(9):
            for c in range(9):
                val = grid[r][c]
                e = self.cells[r][c]
                if val == 0:
                    e.delete(0, tk.END)
                else:
                    e.delete(0, tk.END)
                    e.insert(0, str(val))
                    # highlight solution entries which were empty originally
                    if original_grid and original_grid[r][c] == 0:
                        e.config(fg='blue')
                    else:
                        e.config(fg='black')

    def on_solve(self):
        
        grid = self.read_grid()
        original = [row[:] for row in grid]
        # Validate initial puzzle: no direct violations
        if not self._validate_initial(grid):
            messagebox.showerror("Invalid Puzzle", "The initial grid violates Sudoku rules.")
            return

        solved = solve_backtracking(grid)
        if solved:
            self.write_grid(grid, original_grid=original)
            messagebox.showinfo("Solved", "Sudoku solved successfully!")
        else:
            messagebox.showwarning("No Solution", "No solution exists for the provided puzzle.")

    def _validate_initial(self, grid):
        
        for r in range(9):
            for c in range(9):
                val = grid[r][c]
                if val != 0:
                    # Temporarily clear cell and check validity
                    grid[r][c] = 0
                    if not is_valid(grid, r, c, val):
                        grid[r][c] = val
                        return False
                    grid[r][c] = val
        return True

    def on_clear(self):
        
        for r in range(9):
            for c in range(9):
                e = self.cells[r][c]
                e.delete(0, tk.END)
                e.config(fg='black')

    def load_example(self):
        
        self.write_grid(self._example_grid)
        # original entries should appear black; we'll not color them here

    def print_grid(self):
        
        grid = self.read_grid()
        print("Current Sudoku Grid (0 denotes empty):")
        for row in grid:
            print(row)
        messagebox.showinfo("Printed", "Grid printed to console.")


# If this file is run directly, open the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
