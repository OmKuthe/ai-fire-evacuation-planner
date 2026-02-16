# 🔥 AI Fire Evacuation Planning System

A Traditional Artificial Intelligence based decision support system that dynamically computes the **safest evacuation path** inside a building during fire emergencies using rule-based reasoning and A* search.

This project demonstrates **symbolic AI, knowledge representation, heuristic search, and explainable reasoning** without using Machine Learning.

---

## 📌 Problem Statement

Static evacuation maps fail during real emergencies because fire, smoke and blocked paths change dynamically.

This system acts as an intelligent safety controller that:

* Understands the building environment
* Evaluates danger zones
* Plans the safest escape route
* Explains its decision

---

## 🧠 AI Concepts Used

| Concept                    | Implementation                 |
| -------------------------- | ------------------------------ |
| State Space Representation | Building modeled as grid graph |
| Knowledge Representation   | Fire & smoke safety rules      |
| Inference Engine           | Risk evaluation rules          |
| Heuristic Search           | A* Algorithm                   |
| Planning                   | Safe route computation         |
| Constraint Satisfaction    | Avoid dangerous areas          |
| Explainable AI             | Justifies exit selection       |

---

## 🏗️ System Architecture

User Interface (Streamlit)
↓
Environment Model (Grid World)
↓
Knowledge Base (Safety Rules)
↓
Risk Engine
↓
A* Planner
↓
Reasoning Engine
↓
Decision Explanation

---

## 🎮 Features

* Interactive building editor (click to place fire/walls/smoke)
* Multiple exits supported
* Risk-aware path planning
* Fire proximity detection
* Explainable decision making
* Real-time evacuation simulation

---

## 🖥️ Tech Stack

* Python
* Streamlit
* NumPy
* Pandas
* A* Search Algorithm
* Rule-Based AI

---

## 📂 Project Structure

```
ai-fire-evacuation-planner/
│
├── app.py
├── requirements.txt
│
├── core/
│   ├── environment.py
│   ├── planner.py
│   ├── rules.py
│   └── reasoning.py
│
└── docs/
```

---

## ▶️ Installation & Run

```bash
git clone https://github.com/OmKuthe/ai-fire-evacuation-planner.git
cd ai-fire-evacuation-planner

python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
streamlit run app.py
```

---

## 🚨 How It Works

1. Create building layout
2. Place fire and smoke
3. Add person and exits
4. Run evacuation planner
5. System computes safest path
6. AI explains the decision

---

## 📊 Example Decision Output

Selected Exit: (7, 7)
Reason: Other exits contain smoke and high fire proximity.
Risk Level: Low

---

## 🎯 Educational Purpose

This project demonstrates a real-world application of **Traditional AI (Symbolic AI)** including:

* Search algorithms
* Planning systems
* Knowledge-based systems
* Explainable AI

---

## 👨‍💻 Author

Developed as part of Artificial Intelligence Laboratory coursework.
