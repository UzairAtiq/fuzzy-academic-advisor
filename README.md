# Bahria University FIS Academic Regulations - Source Code Package

## Project Metadata
- **Institution:** Bahria University Islamabad Campus, Department of Computer Science
- **Course:** Knowledge Representation & Reasoning (CS-311) | Fall 2026
- **Instructor:** Ma'am Samabia Tehsin
- **Authors:**
  1. Abdur Rafay (01-136242-004)
  2. Ali Zafar (01-136242-005)
  3. Sanaullah Turab (01-136242-026)
  4. Uzair Attiq (01-136242-029)
  5. Zain Matloob (01-136242-030)

## Code Modules
1. `fuzzy_core.py`: Standalone Mamdani Fuzzy Inference Engine implementing membership functions, t-norms, implication, and defuzzification.
2. `models.py`: Formal mathematical definitions and 50 calibrated fuzzy rules across 4 institutional policy subsystems (§1.27, §1.14, §1.17, §5.5).
3. `gui.py`: Interactive Tkinter graphical user interface with live centroid feedback, alpha-cut explanations, and Student 360 diagnostic.
4. `test_suite.py`: Automated verification harness executing 38 statutory test queries.
5. `plot_generators.py`: Membership function curves and 2D/3D non-linear response surface generators (strictly zero blue styling).
6. `sample_worked_examples.json`: 10 realistic student scenarios with benchmark inputs and outputs.

## How to Run
```bash
# 1. Launch the Graphical Interface
python gui.py

# 2. Run the 38-Query Test Harness
python test_suite.py

# 3. Regenerate Membership Function and Surface Plots
python plot_generators.py
```
