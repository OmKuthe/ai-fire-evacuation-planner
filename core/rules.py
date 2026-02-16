from math import inf

class RiskEngine:
    def __init__(self, env):
        self.env = env

# Manhattan distance
    def dist(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

# --------- Main Risk Function ---------
    def risk_cost(self, r, c):

        cell = self.env.grid[r][c]

        # Fire cell → impossible
        if cell == 'F':
            return inf

        cost = 1   # base movement cost

    # Smoke penalty
        if cell == 'S':
            cost += 5

    # Near fire penalty
        for i in range(self.env.rows):
            for j in range(self.env.cols):
                if self.env.grid[i][j] == 'F':
                    d = self.dist((r,c),(i,j))

                    if d == 1:
                        cost += 20   # extremely dangerous
                    elif d == 2:
                        cost += 10
                    elif d == 3:
                        cost += 4

        return cost
