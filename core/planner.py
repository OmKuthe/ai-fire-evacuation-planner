import heapq
from core.rules import RiskEngine

class EvacuationPlanner:
    def __init__(self, env):
        self.env = env
        self.risk_engine = RiskEngine(env)

    # Manhattan heuristic
    def heuristic(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def neighbors(self, node):
        r, c = node
        moves = [(1,0),(-1,0),(0,1),(0,-1)]
        result = []

        for dr, dc in moves:
            nr, nc = r+dr, c+dc
            if self.env.is_walkable(nr, nc):
                result.append((nr, nc))

        return result

    def reconstruct(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        path.reverse()
        return path

    # -------- MAIN A* SEARCH --------
    def find_path(self, start):
        best_path = None
        best_cost = float('inf')

        for exit in self.env.exits:
            open_set = []
            heapq.heappush(open_set, (0, start))

            came_from = {}
            g_score = {start: 0}

            while open_set:
                _, current = heapq.heappop(open_set)

                if current == exit:
                    path = self.reconstruct(came_from, current)
                    cost = g_score[current]

                    if cost < best_cost:
                        best_cost = cost
                        best_path = path
                    break

                for neighbor in self.neighbors(current):
                    risk = self.risk_engine.risk_cost(*neighbor)
                    tentative = g_score[current] + risk

                    if neighbor not in g_score or tentative < g_score[neighbor]:
                        g_score[neighbor] = tentative
                        priority = tentative + self.heuristic(neighbor, exit)
                        heapq.heappush(open_set, (priority, neighbor))
                        came_from[neighbor] = current

        return best_path, best_cost