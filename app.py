from core.environment import Environment
from core.planner import EvacuationPlanner

env = Environment(8,8)

env.add_fire(3,3)
env.add_fire(3,4)
env.add_smoke(2,3)

env.add_exit(0,7)
env.add_exit(7,7)

env.add_person(7,0)

env.display()

planner = EvacuationPlanner(env)

start = env.people[0]
path, cost = planner.find_path(start)

print("\nChosen Path:", path)
print("Total Cost:", cost)
