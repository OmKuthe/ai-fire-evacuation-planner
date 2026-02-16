from core.rules import RiskEngine
from core.planner import EvacuationPlanner

class ReasoningEngine:
    def __init__(self, env):
        self.env = env
        self.risk = RiskEngine(env)
        self.planner = EvacuationPlanner(env)

    def analyze_exit(self, start, exit):
        path, cost = self.planner.find_path(start)
        if path is None:
            return None

        fire_exposure = 0
        smoke_exposure = 0

        for r, c in path:
            cell = self.env.grid[r][c]

            if cell == 'S':
                smoke_exposure += 1

            # near fire detection
            for i in range(self.env.rows):
                for j in range(self.env.cols):
                    if self.env.grid[i][j] == 'F':
                        d = abs(r-i) + abs(c-j)
                        if d <= 2:
                            fire_exposure += 1

        return {
            "exit": exit,
            "cost": cost,
            "fire_exposure": fire_exposure,
            "smoke_exposure": smoke_exposure,
            "path_length": len(path)
        }

    def explain(self, start):
        analyses = []
        for ex in self.env.exits:
            result = self.analyze_exit(start, ex)
            if result:
                analyses.append(result)

        if not analyses:
            return "No safe path available."

        best = min(analyses, key=lambda x: x["cost"])

        explanation = f"\nSelected Exit: {best['exit']}\n"
        explanation += f"Total Risk Cost: {best['cost']}\n\n"

        for a in analyses:
            explanation += f"Exit {a['exit']} -> Distance:{a['path_length']} "
            explanation += f"Smoke:{a['smoke_exposure']} FireRisk:{a['fire_exposure']}\n"

        explanation += "\nDecision: Chosen exit has lowest combined risk and distance."

        return explanation