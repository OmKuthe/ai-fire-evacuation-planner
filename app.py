from core.environment import Environment
from core.rules import RiskEngine

env = Environment(6,6)

env.add_fire(2,2)
env.add_smoke(1,2)
env.add_exit(0,5)
env.add_person(5,0)

env.display()

print("\nRisk Map:\n")

risk = RiskEngine(env)

for i in range(env.rows):
    for j in range(env.cols):
        print(f"{risk.risk_cost(i,j):3}", end=" ")
    print()
