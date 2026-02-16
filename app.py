import streamlit as st
import numpy as np
import pandas as pd
from core.environment import Environment
from core.planner import EvacuationPlanner
from core.reasoning import ReasoningEngine

# ---------------- PAGE CONFIG ----------------

st.set_page_config(page_title="AI Fire Evacuation Planner", layout="wide")
st.title("🔥 AI Fire Evacuation Planning System")

# ---------------- GRID SIZE ----------------

st.sidebar.header("Environment Settings")

rows = st.sidebar.slider("Rows", 5, 20, 10)
cols = st.sidebar.slider("Columns", 5, 20, 10)

# Initialize grid in session state
if "grid" not in st.session_state:
    st.session_state.grid = np.full((rows, cols), "0", dtype=str)

# If size changed → reset grid
if st.session_state.grid.shape != (rows, cols):
    st.session_state.grid = np.full((rows, cols), "0", dtype=str)

# ---------------- DRAW TOOLS ----------------

st.sidebar.header("Draw Tools")

tool = st.sidebar.radio(
    "Select Tool",
    ["Wall", "Fire", "Smoke", "Exit", "Person", "Erase"]
)

r = st.sidebar.number_input("Row", 0, rows-1, 0)
c = st.sidebar.number_input("Column", 0, cols-1, 0)

symbol_map = {
    "Wall": "W",
    "Fire": "F",
    "Smoke": "S",
    "Exit": "E",
    "Person": "P",
    "Erase": "0"
}

if st.sidebar.button("Apply"):
    st.session_state.grid[r][c] = symbol_map[tool]

# ---------------- CLEAR BUTTON ----------------

if st.sidebar.button("Reset Grid"):
    st.session_state.grid = np.full((rows, cols), "0", dtype=str)

# ---------------- DISPLAY GRID ----------------

st.subheader("Building Layout")

def color_cells(val):
    colors = {
        "W": "background-color: black",
        "F": "background-color: red",
        "S": "background-color: orange",
        "E": "background-color: green",
        "P": "background-color: blue",
        "0": "background-color: white"
    }
    return colors.get(val, "")

styled = pd.DataFrame(st.session_state.grid).style.applymap(color_cells)

st.dataframe(styled, height=500, use_container_width=True)

st.info("Place at least 1 Person and 1 Exit to run evacuation later.")

#---------------- CREATE ENVIRONMENT ----------------

def build_environment(grid):
    rows, cols = grid.shape
    env = Environment(rows, cols)

    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]

            if cell == "W":
                env.add_wall(i, j)
            elif cell == "F":
                env.add_fire(i, j)
            elif cell == "S":
                env.add_smoke(i, j)
            elif cell == "E":
                env.add_exit(i, j)
            elif cell == "P":
                env.add_person(i, j)

    return env

st.subheader("AI Decision")

if st.button("🚨 Run Evacuation Planner"):
    env = build_environment(st.session_state.grid)
    
    if len(env.people) == 0 or len(env.exits) == 0:
        st.error("Add at least one Person and one Exit")
    else:
        planner = EvacuationPlanner(env)
        reasoning = ReasoningEngine(env)
        
        start = env.people[0]
        path, cost = planner.find_path(start)
        
        if path is None:
            st.error("No safe path found!")
        else:
            # Draw path
            path_grid = st.session_state.grid.copy()
            for r, c in path:
                if path_grid[r][c] == "0":
                    path_grid[r][c] = "*"
            
            st.success("Path Found!")
            
            # Display path grid
            def color_path(val):
                colors = {
                    "W": "background-color: black",
                    "F": "background-color: red",
                    "S": "background-color: orange",
                    "E": "background-color: green",
                    "P": "background-color: blue",
                    "*": "background-color: purple",
                    "0": "background-color: white"
                }
                return colors.get(val, "")
            
            styled_path = pd.DataFrame(path_grid).style.applymap(color_path)
            st.dataframe(styled_path, height=500, use_container_width=True)
            
            # Explanation
            explanation = reasoning.explain(start)
            st.text(explanation)