import streamlit as st
import numpy as np
import pandas as pd
import time

from core.environment import Environment
from core.planner import EvacuationPlanner
from core.reasoning import ReasoningEngine

# ---------------- PAGE CONFIG ----------------

st.set_page_config(page_title="AI Fire Evacuation Planner", layout="wide")
st.title("🔥 AI Fire Evacuation Planning System")

# ---------------- GRID SIZE ----------------

st.sidebar.header("Environment Settings")
rows = st.sidebar.slider("Rows", 5, 10, 5)  # Limited to 10 for better display
cols = st.sidebar.slider("Columns", 5, 10, 5)

# Initialize grid and state
if "grid" not in st.session_state:
    st.session_state.grid = np.full((rows, cols), "0", dtype=str)
    st.session_state.animating = False
    st.session_state.animation_step = 0
    st.session_state.path = None
    st.session_state.selected_cell = None

# Reset if size changed
if st.session_state.grid.shape != (rows, cols):
    st.session_state.grid = np.full((rows, cols), "0", dtype=str)
    st.session_state.animating = False
    st.session_state.animation_step = 0
    st.session_state.path = None
    st.session_state.selected_cell = None

# ---------------- TOOL SELECTOR ----------------

st.sidebar.header("Cell Editor")

# Display selected cell info
if st.session_state.selected_cell:
    r, c = st.session_state.selected_cell
    current_value = st.session_state.grid[r][c]
    value_names = {"W": "Wall", "F": "Fire", "S": "Smoke", "E": "Exit", "P": "Person", "0": "Empty"}
    current_name = value_names.get(current_value, "Unknown")
    
    st.sidebar.success(f"✅ Selected: Row {r}, Col {c}")
    st.sidebar.info(f"Current: {current_name} ({current_value})")
else:
    st.sidebar.info("Click on any cell below to select it")

# Tool selection
tool = st.sidebar.radio(
    "Choose element to place:",
    ["Wall", "Fire", "Smoke", "Exit", "Person", "Erase"]
)

symbol_map = {
    "Wall": "W",
    "Fire": "F",
    "Smoke": "S",
    "Exit": "E",
    "Person": "P",
    "Erase": "0"
}

# Apply button
if st.sidebar.button("✅ Apply to Selected Cell"):
    if st.session_state.selected_cell:
        r, c = st.session_state.selected_cell
        st.session_state.grid[r][c] = symbol_map[tool]
        st.session_state.selected_cell = None  # Deselect after applying
        st.rerun()
    else:
        st.sidebar.error("Please select a cell first!")

# ---------------- RESET BUTTON ----------------

st.sidebar.header("Grid Controls")
if st.sidebar.button("🔄 Reset Grid"):
    st.session_state.grid = np.full((rows, cols), "0", dtype=str)
    st.session_state.animating = False
    st.session_state.animation_step = 0
    st.session_state.path = None
    st.session_state.selected_cell = None
    st.rerun()

# ---------------- ANIMATION CONTROLS ----------------

st.sidebar.header("Animation Controls")
animation_speed = st.sidebar.slider("Animation Speed (seconds)", 0.1, 1.0, 0.3)

if st.sidebar.button("⏹️ Stop Animation"):
    st.session_state.animating = False
    st.session_state.animation_step = 0
    st.rerun()

# ---------------- MAIN GRID ----------------

st.subheader("Interactive Building Grid")

# Create a grid of buttons
grid_display = st.container()

with grid_display:
    # Create column headers
    cols_header = st.columns([0.5] + [1] * cols)
    with cols_header[0]:
        st.markdown("**R\C**")
    for j in range(cols):
        with cols_header[j + 1]:
            st.markdown(f"**{j}**")
    
    # Create rows with buttons
    for i in range(rows):
        row_cols = st.columns([0.5] + [1] * cols)
        
        # Row number
        with row_cols[0]:
            st.markdown(f"**{i}**")
        
        # Cells
        for j in range(cols):
            with row_cols[j + 1]:
                cell_value = st.session_state.grid[i][j]
                
                # Determine button color based on cell value
                if cell_value == "W":
                    button_color = "black"
                    text_color = "white"
                    emoji = "🧱"
                elif cell_value == "F":
                    button_color = "red"
                    text_color = "white"
                    emoji = "🔥"
                elif cell_value == "S":
                    button_color = "orange"
                    text_color = "black"
                    emoji = "💨"
                elif cell_value == "E":
                    button_color = "green"
                    text_color = "white"
                    emoji = "🚪"
                elif cell_value == "P":
                    button_color = "blue"
                    text_color = "white"
                    emoji = "👤"
                else:
                    button_color = "white"
                    text_color = "black"
                    emoji = "⬜"
                
                # Create a unique key for each button
                button_key = f"cell_{i}_{j}"
                
                # Create the button with custom styling
                if st.button(
                    emoji,
                    key=button_key,
                    help=f"Row {i}, Col {j} - Click to select",
                    use_container_width=True
                ):
                    st.session_state.selected_cell = (i, j)
                    st.rerun()

# ---------------- ENVIRONMENT BUILDER ----------------

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

# ---------------- RUN AI ----------------

st.subheader("AI Decision")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🚨 Run Evacuation Planner", use_container_width=True):
        env = build_environment(st.session_state.grid)
        
        if len(env.people) == 0:
            st.error("Add at least one Person (👤)")
        elif len(env.exits) == 0:
            st.error("Add at least one Exit (🚪)")
        else:
            planner = EvacuationPlanner(env)
            reasoning = ReasoningEngine(env)
            
            start = env.people[0]
            path, cost = planner.find_path(start)
            
            if path is None:
                st.error("No safe path found!")
            else:
                st.session_state.path = path
                st.session_state.animating = True
                st.session_state.animation_step = 0
                st.rerun()

with col2:
    if st.button("⏯️ Replay Animation", use_container_width=True) and st.session_state.path is not None:
        st.session_state.animating = True
        st.session_state.animation_step = 0
        st.rerun()

# ---------------- ANIMATION DISPLAY ----------------

# Create placeholders
animation_placeholder = st.empty()
explanation_placeholder = st.empty()

# Handle animation
if st.session_state.animating and st.session_state.path is not None:
    path = st.session_state.path
    
    # Create a copy of the original grid
    display_grid = st.session_state.grid.copy()
    
    # Show path up to current animation step
    for i, (r, c) in enumerate(path):
        if i <= st.session_state.animation_step:
            if display_grid[r][c] == "0":  # Don't override existing elements
                display_grid[r][c] = "*"
    
    # Display animated grid with custom styling
    st.subheader("Evacuation Path Animation")
    
    # Create a styled DataFrame for display
    def highlight_cells(val):
        if val == "W":
            return 'background-color: black; color: white'
        elif val == "F":
            return 'background-color: red; color: white'
        elif val == "S":
            return 'background-color: orange; color: black'
        elif val == "E":
            return 'background-color: green; color: white'
        elif val == "P":
            return 'background-color: blue; color: white'
        elif val == "*":
            return 'background-color: purple; color: white; font-weight: bold'
        else:
            return 'background-color: white; color: black'
    
    df_display = pd.DataFrame(display_grid)
    styled_df = df_display.style.applymap(highlight_cells)
    
    animation_placeholder.dataframe(styled_df, height=400, use_container_width=True)
    
    # Show progress
    progress = (st.session_state.animation_step + 1) / len(path)
    st.progress(progress)
    st.caption(f"Step {st.session_state.animation_step + 1} of {len(path)}")
    
    # Increment animation step
    if st.session_state.animation_step < len(path) - 1:
        time.sleep(animation_speed)
        st.session_state.animation_step += 1
        st.rerun()
    else:
        st.session_state.animating = False
        # Show final explanation
        env = build_environment(st.session_state.grid)
        reasoning = ReasoningEngine(env)
        start = env.people[0] if len(env.people) > 0 else None
        if start:
            explanation = reasoning.explain(start)
            explanation_placeholder.text_area("Analysis", explanation, height=200)
else:
    # Display current grid
    if st.session_state.path is not None and not st.session_state.animating:
        # Show full path
        display_grid = st.session_state.grid.copy()
        for r, c in st.session_state.path:
            if display_grid[r][c] == "0":
                display_grid[r][c] = "*"
        
        def highlight_cells(val):
            if val == "W":
                return 'background-color: black; color: white'
            elif val == "F":
                return 'background-color: red; color: white'
            elif val == "S":
                return 'background-color: orange; color: black'
            elif val == "E":
                return 'background-color: green; color: white'
            elif val == "P":
                return 'background-color: blue; color: white'
            elif val == "*":
                return 'background-color: purple; color: white; font-weight: bold'
            else:
                return 'background-color: white; color: black'
        
        df_display = pd.DataFrame(display_grid)
        styled_df = df_display.style.applymap(highlight_cells)
        animation_placeholder.dataframe(styled_df, height=400, use_container_width=True)
        
        # Show explanation
        env = build_environment(st.session_state.grid)
        reasoning = ReasoningEngine(env)
        start = env.people[0] if len(env.people) > 0 else None
        if start:
            explanation = reasoning.explain(start)
            explanation_placeholder.text_area("Analysis", explanation, height=200)
    else:
        # Show current grid
        def highlight_cells(val):
            if val == "W":
                return 'background-color: black; color: white'
            elif val == "F":
                return 'background-color: red; color: white'
            elif val == "S":
                return 'background-color: orange; color: black'
            elif val == "E":
                return 'background-color: green; color: white'
            elif val == "P":
                return 'background-color: blue; color: white'
            else:
                return 'background-color: white; color: black'
        
        df_display = pd.DataFrame(st.session_state.grid)
        styled_df = df_display.style.applymap(highlight_cells)
        animation_placeholder.dataframe(styled_df, height=400, use_container_width=True)

# ---------------- LEGEND ----------------

st.sidebar.markdown("---")
st.sidebar.subheader("Legend")
st.sidebar.markdown("🧱 **Wall** - Black")
st.sidebar.markdown("🔥 **Fire** - Red")
st.sidebar.markdown("💨 **Smoke** - Orange")
st.sidebar.markdown("🚪 **Exit** - Green")
st.sidebar.markdown("👤 **Person** - Blue")
st.sidebar.markdown("⬜ **Empty** - White")
st.sidebar.markdown("🟪 **Path** - Purple")

# Instructions
st.info("""
📝 **Instructions:**
1. Click on any cell in the grid above to select it
2. The selected cell coordinates will appear in the sidebar
3. Choose an element from the sidebar (Wall, Fire, Smoke, Exit, Person, or Erase)
4. Click 'Apply to Selected Cell' to place the element
5. Place at least 1 Person (👤) and 1 Exit (🚪)
6. Click 'Run Evacuation Planner' to find and animate the safest path
""")