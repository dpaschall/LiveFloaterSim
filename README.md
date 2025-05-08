# Live_Sim_Proj

Project folder outline for magnetic simulation and animation.

Live_Sim_Proj/
├── README.md
├── requirements.txt
├── config.json
│
├── notebooks/
│   ├── 01_Config_Inputs.ipynb
│   ├── 02_Geometry_Diagram.ipynb
│   ├── 03_Symbolic_Equations.ipynb
│   ├── 04_Run_Simulation.ipynb
│   ├── 05_PostProcess_Animation.ipynb
│   └── Main_Simulator.ipynb
│
├── src/
│   ├── __init__.py
│   └── simulator.py
│
└── results/
    ├── axis_vecs.npz
    ├── sim_output.csv
    ├── cylinder_animation.gif
    ├── geometry_diagram.png
    ├── eom_exprs.pkl
    └── initial_conditions.npz
