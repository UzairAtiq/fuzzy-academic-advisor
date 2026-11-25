"""
========================================================================================
BAHRIA UNIVERSITY ISLAMABAD CAMPUS - DEPARTMENT OF COMPUTER SCIENCE
Course: Knowledge Representation & Reasoning (CS-311) | Semester 05 (Fall 2026)
Instructor: Ma'am Samabia Tehsin
Project: Fuzzy Inference System (FIS) for University Academic Regulations
----------------------------------------------------------------------------------------
Student Group Members:
  1. Abdur Rafay      (01-136242-004) - Group Lead / Fuzzy Inference Core
  2. Ali Zafar        (01-136242-005) - Policy Subsystems & Rule Calibration
  3. Sanaullah Turab  (01-136242-026) - GUI Architecture & Response Surfaces
  4. Uzair Attiq      (01-136242-029) - Automated Test Suite & Evaluation Harness
  5. Zain Matloob     (01-136242-030) - Technical Report & Presentation
========================================================================================
"""

"""
Generates visual plots of:
1. All Input and Output Membership Functions for all 4 policy subsystems.
2. 3D / 2D Fuzzy Output Surfaces showing inference mapping and boundary transitions.
NO BLUE COLORS USED (Neutral Charcoal, Forest Green, Amber, Purple, Deep Crimson).
NO LONG DASHES.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from models import (build_attendance_subsystem, build_withdrawal_subsystem,
                    build_repeat_subsystem, build_probation_subsystem)

os.makedirs("figures", exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

def plot_subsystem_mfs(subsystem, filename_prefix):
    """Plots input and output membership functions for a given subsystem without blue."""
    all_vars = list(subsystem.inputs.items()) + list(subsystem.outputs.items())
    num_vars = len(all_vars)
    
    fig, axes = plt.subplots(num_vars, 1, figsize=(9, 2.8 * num_vars), constrained_layout=True)
    if num_vars == 1:
        axes = [axes]

    # Non-blue palette: Dark Charcoal, Forest Green, Warm Amber, Purple, Deep Crimson
    colors = ['#2E7D32', '#D97706', '#7B1FA2', '#C53030', '#262626']

    for idx, (var_name, var) in enumerate(all_vars):
        ax = axes[idx]
        x_min, x_max = var.universe
        x = np.linspace(x_min, x_max, 600)
        
        is_input = var_name in subsystem.inputs
        var_type = "INPUT" if is_input else "OUTPUT"
        
        for c_idx, (term_name, mf) in enumerate(var.terms.items()):
            y = np.array([mf(val) for val in x])
            color = colors[c_idx % len(colors)]
            ax.plot(x, y, label=term_name.replace('_', ' '), linewidth=2.2, color=color)
            ax.fill_between(x, 0, y, alpha=0.12, color=color)

        ax.set_title(f"{var_type}: {var_name.replace('_', ' ')} [{var.unit}]", fontsize=11, fontweight='bold', pad=8, color='#1A1A1A')
        ax.set_xlabel(f"{var_name.replace('_', ' ')} ({var.unit})", fontsize=10, color='#1A1A1A')
        ax.set_ylabel("Degree of Membership (mu)", fontsize=10, color='#1A1A1A')
        ax.set_ylim(-0.05, 1.1)
        ax.set_xlim(x_min, x_max)
        ax.legend(loc="upper right", frameon=True, fontsize=9)
        ax.grid(True, linestyle=":", alpha=0.6, color='#CCCCCC')

    fig.suptitle(f"Membership Functions: {subsystem.name}", fontsize=13, fontweight='bold', color='#1A1A1A')
    out_path = os.path.join("figures", f"{filename_prefix}_mfs.png")
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"Generated: {out_path}")

def plot_surfaces():
    """Generates 3D and 2D response surfaces without blue colors."""
    # 1. Attendance: Attendance Pct vs Debarment Risk
    att_sys = build_attendance_subsystem()
    x_att = np.linspace(50, 100, 100)
    y_risk = []
    y_elig = []
    for val in x_att:
        res = att_sys.infer({"Attendance_Pct": val, "Remedial_Makeup_Score": 0.0})
        y_risk.append(res["crisp_outputs"]["Debarment_Risk"])
        y_elig.append(res["crisp_outputs"]["Exam_Eligibility"])

    fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
    ax.plot(x_att, y_risk, label="Debarment Risk Index", color="#C53030", linewidth=2.5)
    ax.plot(x_att, y_elig, label="Exam Eligibility Index", color="#2E7D32", linewidth=2.5)
    ax.axvline(75, color="#1A1A1A", linestyle="--", linewidth=1.5, label="Handbook 75% Cutoff")
    ax.axvspan(70, 78, color="#FADBD8", alpha=0.35, label="Fuzzy Transition Region (70 to 78%)")
    ax.set_title("Attendance Policy Fuzzy Mapping (Section 1.27)", fontsize=12, fontweight='bold', color='#1A1A1A')
    ax.set_xlabel("Attendance Percentage (%)", fontsize=11, color='#1A1A1A')
    ax.set_ylabel("Fuzzy Output Index (0 to 100)", fontsize=11, color='#1A1A1A')
    ax.legend(loc="center left", frameon=True)
    ax.grid(True, linestyle=":", alpha=0.7, color='#CCCCCC')
    fig.savefig(os.path.join("figures", "surface_attendance.png"), dpi=200)
    plt.close(fig)

    # 2. Withdrawal: Days vs Refund & Transcript Impact (Green & Amber/Orange, no blue)
    wdl_sys = build_withdrawal_subsystem()
    days = np.linspace(0, 65, 130)
    refunds = []
    penalties = []
    for d in days:
        res = wdl_sys.infer({"Withdrawal_Day": d})
        refunds.append(res["crisp_outputs"]["Fee_Refund_Adjustment_Pct"])
        penalties.append(res["crisp_outputs"]["Transcript_Penalty_Severity"])

    fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
    ax.plot(days, refunds, label="Fee Refund %", color="#2E7D32", linewidth=2.5)
    ax.plot(days, penalties, label="Transcript Severity", color="#D97706", linewidth=2.5)
    ax.axvline(7, color="#1E7E34", linestyle=":", label="Day 7 (End of Week 1)")
    ax.axvline(15, color="#E65100", linestyle=":", label="Day 15 (Half Refund Cutoff)")
    ax.axvline(49, color="#C53030", linestyle=":", label="Day 49 (End of Week 7 Cutoff)")
    ax.set_title("Course Withdrawal Timeline Mapping (Section 1.14)", fontsize=12, fontweight='bold', color='#1A1A1A')
    ax.set_xlabel("Days Elapsed Since Commencement of Semester", fontsize=11, color='#1A1A1A')
    ax.set_ylabel("Output Index / Percentage", fontsize=11, color='#1A1A1A')
    ax.legend(loc="center right", frameon=True)
    ax.grid(True, linestyle=":", alpha=0.7, color='#CCCCCC')
    fig.savefig(os.path.join("figures", "surface_withdrawal.png"), dpi=200)
    plt.close(fig)

    # 3. Probation 3D Surface: magma colormap (black, red, orange, yellow - NO BLUE)
    prb_sys = build_probation_subsystem()
    margins = np.linspace(-1.5, 1.5, 40)
    probs = np.linspace(0, 2.5, 30)
    M, P = np.meshgrid(margins, probs)
    Z_risk = np.zeros_like(M)

    for i in range(len(probs)):
        for j in range(len(margins)):
            res = prb_sys.infer({"CGPA_Margin": M[i, j], "Consecutive_Probations": P[i, j]})
            Z_risk[i, j] = res["crisp_outputs"]["Academic_Risk_Severity"]

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(M, P, Z_risk, cmap='magma', edgecolor='none', alpha=0.85)
    ax.set_title("3D Academic Standing & Drop Threat Surface (Section 5.5)", fontsize=12, fontweight='bold', pad=12, color='#1A1A1A')
    ax.set_xlabel("CGPA Margin (CGPA - Min)", fontsize=10, labelpad=8, color='#1A1A1A')
    ax.set_ylabel("Consecutive Probations", fontsize=10, labelpad=8, color='#1A1A1A')
    ax.set_zlabel("Academic Risk Severity", fontsize=10, labelpad=8, color='#1A1A1A')
    fig.colorbar(surf, ax=ax, shrink=0.55, aspect=10, label="Risk Index (0 to 100)")
    fig.tight_layout()
    fig.savefig(os.path.join("figures", "surface_probation_3d.png"), dpi=200)
    plt.close(fig)

    # 4. Repeat Course 3D Surface: plasma / inferno colormap (NO BLUE)
    rep_sys = build_repeat_subsystem()
    gpas = np.linspace(0.0, 3.5, 35)
    sizes = np.linspace(2, 25, 30)
    G, S = np.meshgrid(gpas, sizes)
    Z_perm = np.zeros_like(G)

    for i in range(len(sizes)):
        for j in range(len(gpas)):
            res = rep_sys.infer({"Earned_Course_GPA": G[i, j], "Cohort_Enrolled_Size": S[i, j]})
            Z_perm[i, j] = res["crisp_outputs"]["Repeat_Permission_Index"]

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(G, S, Z_perm, cmap='inferno', edgecolor='none', alpha=0.85)
    ax.set_title("3D Course Repeat Permission Surface (Section 1.17)", fontsize=12, fontweight='bold', pad=12, color='#1A1A1A')
    ax.set_xlabel("Earned Grade Point (GP)", fontsize=10, labelpad=8, color='#1A1A1A')
    ax.set_ylabel("Cohort Size Enrolled", fontsize=10, labelpad=8, color='#1A1A1A')
    ax.set_zlabel("Permission Index", fontsize=10, labelpad=8, color='#1A1A1A')
    fig.colorbar(surf, ax=ax, shrink=0.55, aspect=10, label="Permission Index (0 to 100)")
    fig.tight_layout()
    fig.savefig(os.path.join("figures", "surface_repeat_3d.png"), dpi=200)
    plt.close(fig)

if __name__ == "__main__":
    plot_subsystem_mfs(build_attendance_subsystem(), "subsystem1_attendance")
    plot_subsystem_mfs(build_withdrawal_subsystem(), "subsystem2_withdrawal")
    plot_subsystem_mfs(build_repeat_subsystem(), "subsystem3_repeat")
    plot_subsystem_mfs(build_probation_subsystem(), "subsystem4_probation")
    plot_surfaces()
    print("All membership function and surface plots successfully regenerated without blue color!")
