import streamlit as st

st.title("AI Fire Evacuation Planner")
st.write("System Initialized Successfully")

from core.environment import Environment

env = Environment(8, 8)

env.add_wall(2,2)
env.add_fire(3,3)
env.add_smoke(4,4)
env.add_exit(0,7)
env.add_person(7,0)

env.display()
