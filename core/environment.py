import numpy as np

class Environment:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=object)

        # initialize empty cells
        for i in range(rows):
            for j in range(cols):
                self.grid[i][j] = 0

        self.exits = []
        self.people = []

    # ---------- Placement Functions ----------

    def add_wall(self, r, c):
        self.grid[r][c] = 1

    def add_fire(self, r, c):
        self.grid[r][c] = 'F'

    def add_smoke(self, r, c):
        self.grid[r][c] = 'S'

    def add_exit(self, r, c):
        self.grid[r][c] = 'E'
        self.exits.append((r, c))

    def add_person(self, r, c):
        self.grid[r][c] = 'P'
        self.people.append((r, c))

    # ---------- Utility ----------

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_walkable(self, r, c):
        if not self.in_bounds(r, c):
            return False
        return self.grid[r][c] != 1 and self.grid[r][c] != 'F'

    def display(self):
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))