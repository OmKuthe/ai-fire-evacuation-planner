from core.environment import Environment
from core.reasoning import ReasoningEngine

env = Environment(8,8)

env.add_fire(3,3)
env.add_smoke(2,3)

env.add_exit(0,7)
env.add_exit(7,7)

env.add_person(7,0)

env.display()

engine = ReasoningEngine(env)

start = env.people[0]
print(engine.explain(start))
