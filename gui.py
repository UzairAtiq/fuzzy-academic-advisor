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
Bahria University Academic Regulations - Fuzzy Advisory System GUI
Interactive Graphical Interface built with Tkinter and Matplotlib.
Supports all 4 Handbook Policy Subsystems + Unified Student Profile.
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from models import (build_attendance_subsystem, build_withdrawal_subsystem,
                    build_repeat_subsystem, build_probation_subsystem,
                    PROGRAM_MIN_CGPA)

class FuzzyAdvisorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bahria University Fuzzy Advisory System - Academic Regulations Expert")
        self.root.geometry("1100x780")
        self.root.minsize(980, 680)

        # Initialize subsystems
        self.att_sys = build_attendance_subsystem()
        self.wdl_sys = build_withdrawal_subsystem()
        self.rep_sys = build_repeat_subsystem()
        self.prb_sys = build_probation_subsystem()

        # Apply ttk theme and styles
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception:
            pass

        self._configure_styles()
        self._build_header()
        self._build_notebook()

    def _configure_styles(self):
        self.style.configure(".", font=('Segoe UI', 10))
        self.style.configure("TNotebook.Tab", font=('Segoe UI', 10, 'bold'), padding=[12, 6])
        self.style.configure("Header.TLabel", font=('Segoe UI', 15, 'bold'), foreground="#222222")
        self.style.configure("SubHeader.TLabel", font=('Segoe UI', 9), foreground="#555555")
        self.style.configure("CardTitle.TLabel", font=('Segoe UI', 11, 'bold'), foreground="#333333")
        self.style.configure("Accent.TButton", font=('Segoe UI', 10, 'bold'), background="#27AE60", foreground="white")
        self.style.map("Accent.TButton", background=[('active', '#1E8449')])
        self.style.configure("Success.TLabel", font=('Segoe UI', 11, 'bold'), foreground="#27AE60")
        self.style.configure("Warning.TLabel", font=('Segoe UI', 11, 'bold'), foreground="#D35400")
        self.style.configure("Danger.TLabel", font=('Segoe UI', 11, 'bold'), foreground="#C0392B")

    def _build_header(self):
        header_frame = ttk.Frame(self.root, padding="15 10 15 5")
        header_frame.pack(fill=tk.X)

        title_lbl = ttk.Label(header_frame, text="Bahria University - Student Regulations Fuzzy Expert System", style="Header.TLabel")
        title_lbl.pack(anchor=tk.W)

        subtitle_lbl = ttk.Label(
            header_frame,
            text="Knowledge Representation & Reasoning (Semester 05) | Grounded in Student Handbook Spring 2026",
            style="SubHeader.TLabel"
        )
        subtitle_lbl.pack(anchor=tk.W)
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=5)

    def _build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Tab 1: Probation & Drop Rules
        self.tab_probation = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_probation, text="1. Probation & Drop (Sec 5.5)")
        self._setup_probation_tab()

        # Tab 2: Attendance & Exam Eligibility
        self.tab_attendance = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_attendance, text="2. Attendance & Exam (Sec 1.27)")
        self._setup_attendance_tab()

        # Tab 3: Course Withdrawal & Fee Refund
        self.tab_withdrawal = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_withdrawal, text="3. Withdrawal & Fee (Sec 1.14)")
        self._setup_withdrawal_tab()

        # Tab 4: Repeating a Course
        self.tab_repeat = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_repeat, text="4. Course Repeat (Sec 1.17)")
        self._setup_repeat_tab()

        # Tab 5: Unified Student Profile
        self.tab_unified = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_unified, text="5. Unified Student 360 Evaluation")
        self._setup_unified_tab()

    # =========================================================================
    # TAB 1: Probation and Drop
    # =========================================================================
    def _setup_probation_tab(self):
        pane = ttk.PanedWindow(self.tab_probation, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.LabelFrame(pane, text="Student Academic Standing Inputs", padding=15)
        pane.add(left_frame, weight=1)

        ttk.Label(left_frame, text="Select Degree Program:").pack(anchor=tk.W, pady=(0, 2))
        self.prb_prog_var = tk.StringVar(value="BS / BBA / BEE")
        prog_cb = ttk.Combobox(left_frame, textvariable=self.prb_prog_var, state="readonly",
                               values=list(PROGRAM_MIN_CGPA.keys()))
        prog_cb.pack(fill=tk.X, pady=(0, 10))
        prog_cb.bind("<<ComboboxSelected>>", lambda e: self._on_prob_prog_changed())

        self.prb_min_lbl = ttk.Label(left_frame, text="Handbook Program Minimum CGPA: 2.00", font=('Segoe UI', 9, 'italic'), foreground="#27AE60")
        self.prb_min_lbl.pack(anchor=tk.W, pady=(0, 12))

        ttk.Label(left_frame, text="Current Cumulative GPA (CGPA):").pack(anchor=tk.W, pady=(0, 2))
        self.prb_cgpa_var = tk.DoubleVar(value=2.15)
        self.prb_cgpa_scale = ttk.Scale(left_frame, from_=0.0, to=4.0, variable=self.prb_cgpa_var, orient=tk.HORIZONTAL,
                                        command=lambda v: self.prb_cgpa_entry.delete(0, tk.END) or self.prb_cgpa_entry.insert(0, f"{float(v):.2f}"))
        self.prb_cgpa_scale.pack(fill=tk.X)
        self.prb_cgpa_entry = ttk.Entry(left_frame, width=8)
        self.prb_cgpa_entry.insert(0, "2.15")
        self.prb_cgpa_entry.pack(anchor=tk.W, pady=(2, 12))

        ttk.Label(left_frame, text="Consecutive Probations on Record (0, 1, or 2):").pack(anchor=tk.W, pady=(0, 2))
        self.prb_count_var = tk.IntVar(value=0)
        prob_spin = ttk.Spinbox(left_frame, from_=0, to=3, textvariable=self.prb_count_var, width=6)
        prob_spin.pack(anchor=tk.W, pady=(0, 15))

        calc_btn = ttk.Button(left_frame, text="Evaluate Academic Standing", style="Accent.TButton", command=self.eval_probation)
        calc_btn.pack(fill=tk.X, pady=8)

        # Right frame: Results
        right_frame = ttk.LabelFrame(pane, text="Fuzzy Reasoning & Standing Decision", padding=15)
        pane.add(right_frame, weight=2)

        self.prb_result_text = tk.Text(right_frame, wrap=tk.WORD, font=('Consolas', 10), height=14)
        self.prb_result_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Bottom plot frame
        self.prb_plot_frame = ttk.Frame(right_frame)
        self.prb_plot_frame.pack(fill=tk.BOTH, expand=True)

        self.eval_probation()

    def _on_prob_prog_changed(self):
        prog = self.prb_prog_var.get()
        min_gpa = PROGRAM_MIN_CGPA.get(prog, 2.00)
        self.prb_min_lbl.config(text=f"Handbook Program Minimum CGPA: {min_gpa:.2f}")

    def eval_probation(self):
        try:
            cgpa = float(self.prb_cgpa_entry.get())
        except ValueError:
            cgpa = self.prb_cgpa_var.get()
        
        prog = self.prb_prog_var.get()
        min_gpa = PROGRAM_MIN_CGPA.get(prog, 2.00)
        consec = float(self.prb_count_var.get())
        margin = round(cgpa - min_gpa, 2)

        res = self.prb_sys.infer({"CGPA_Margin": margin, "Consecutive_Probations": consec})
        
        risk = res["crisp_outputs"]["Academic_Risk_Severity"]
        action = res["crisp_outputs"]["Registration_Action_Advisory"]
        risk_label = res["linguistic_labels"]["Academic_Risk_Severity"]
        action_label = res["linguistic_labels"]["Registration_Action_Advisory"]

        self.prb_result_text.delete('1.0', tk.END)
        self.prb_result_text.insert(tk.END, "====================================================================\n")
        self.prb_result_text.insert(tk.END, f"BAHRIA UNIVERSITY ACADEMIC STANDING EVALUATION (SECTION 5.5)\n")
        self.prb_result_text.insert(tk.END, f"Program: {prog} | Min Required CGPA: {min_gpa:.2f}\n")
        self.prb_result_text.insert(tk.END, f"Current CGPA: {cgpa:.2f} | Margin (Delta): {margin:+.2f} | Consecutive Probations: {int(consec)}\n")
        self.prb_result_text.insert(tk.END, "--------------------------------------------------------------------\n")
        self.prb_result_text.insert(tk.END, f"CRISP ACADEMIC RISK SCORE:    {risk:.2f} / 100  --> [{risk_label.replace('_', ' ')}]\n")
        self.prb_result_text.insert(tk.END, f"CRISP REGISTRATION CLEARANCE: {action:.2f} / 100 --> [{action_label.replace('_', ' ')}]\n")
        self.prb_result_text.insert(tk.END, "--------------------------------------------------------------------\n")
        self.prb_result_text.insert(tk.END, "REGULATION ACTION SUMMARY:\n")
        if consec >= 2 and margin < 0:
            self.prb_result_text.insert(tk.END, "CRITICAL ALERT: Student failed to achieve minimum CGPA after 2 consecutive probations.\n")
            self.prb_result_text.insert(tk.END, "Handbook Sec 5.5.3: MANDATORY DROP from academic programme. Cannot register.\n")
        elif consec >= 2 and margin >= 0:
            self.prb_result_text.insert(tk.END, "STATUS RESTORED: CGPA meets/exceeds minimum. Handbook Sec 5.5.4 applies:\n")
            self.prb_result_text.insert(tk.END, "Probation count is officially RESET TO ZERO for leftover semesters.\n")
        elif margin < 0 and consec == 1:
            self.prb_result_text.insert(tk.END, "WARNING: Placed on 2nd Probation. Handbook Sec 5.5.5: Must obtain prior approval\n")
            self.prb_result_text.insert(tk.END, "from Principal through HoD before registering for any new course/semester.\n")
        elif margin < 0 and consec == 0:
            self.prb_result_text.insert(tk.END, "PROBATION NOTICE: CGPA below threshold. Placed on 1st Probation.\n")
            self.prb_result_text.insert(tk.END, "Handbook Sec 5.5.2: Formal warning letter to be issued by HoD.\n")
        else:
            self.prb_result_text.insert(tk.END, "GOOD STANDING: CGPA satisfies university academic requirements. Unrestricted enrollment.\n")
        
        self.prb_result_text.insert(tk.END, "\nFIRED FUZZY RULES (With Activation Strengths):\n")
        for r in res["fired_rules"]:
            self.prb_result_text.insert(tk.END, f" - [{r['rule_id']}] α = {r['strength']:.3f} | {r['description']}\n")

    # =========================================================================
    # TAB 2: Attendance & Exam Eligibility
    # =========================================================================
    def _setup_attendance_tab(self):
        pane = ttk.PanedWindow(self.tab_attendance, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.LabelFrame(pane, text="Course Attendance Inputs", padding=15)
        pane.add(left_frame, weight=1)

        ttk.Label(left_frame, text="Attendance Percentage (%):").pack(anchor=tk.W, pady=(0, 2))
        self.att_val_var = tk.DoubleVar(value=74.0)
        ttk.Scale(left_frame, from_=0.0, to=100.0, variable=self.att_val_var, orient=tk.HORIZONTAL,
                  command=lambda v: self.att_entry.delete(0, tk.END) or self.att_entry.insert(0, f"{float(v):.1f}")).pack(fill=tk.X)
        self.att_entry = ttk.Entry(left_frame, width=8)
        self.att_entry.insert(0, "74.0")
        self.att_entry.pack(anchor=tk.W, pady=(2, 12))

        ttk.Label(left_frame, text="Approved Sports/Event Makeup Tutorial (Sec 1.27.2):").pack(anchor=tk.W, pady=(0, 2))
        ttk.Label(left_frame, text="(0 = None/Unapproved, 5 = Partial, 10 = Fully Certified)", font=('Segoe UI', 8, 'italic')).pack(anchor=tk.W)
        self.att_tut_var = tk.DoubleVar(value=0.0)
        ttk.Scale(left_frame, from_=0.0, to=10.0, variable=self.att_tut_var, orient=tk.HORIZONTAL,
                  command=lambda v: self.att_tut_entry.delete(0, tk.END) or self.att_tut_entry.insert(0, f"{float(v):.1f}")).pack(fill=tk.X)
        self.att_tut_entry = ttk.Entry(left_frame, width=8)
        self.att_tut_entry.insert(0, "0.0")
        self.att_tut_entry.pack(anchor=tk.W, pady=(2, 15))

        calc_btn = ttk.Button(left_frame, text="Evaluate Exam Eligibility", style="Accent.TButton", command=self.eval_attendance)
        calc_btn.pack(fill=tk.X, pady=8)

        right_frame = ttk.LabelFrame(pane, text="Exam Eligibility & Debarment Risk Assessment", padding=15)
        pane.add(right_frame, weight=2)

        self.att_result_text = tk.Text(right_frame, wrap=tk.WORD, font=('Consolas', 10), height=18)
        self.att_result_text.pack(fill=tk.BOTH, expand=True)

        self.eval_attendance()

    def eval_attendance(self):
        try:
            att = float(self.att_entry.get())
        except ValueError:
            att = self.att_val_var.get()
        try:
            tut = float(self.att_tut_entry.get())
        except ValueError:
            tut = self.att_tut_var.get()

        res = self.att_sys.infer({"Attendance_Pct": att, "Remedial_Makeup_Score": tut})
        risk = res["crisp_outputs"]["Debarment_Risk"]
        elig = res["crisp_outputs"]["Exam_Eligibility"]
        risk_lbl = res["linguistic_labels"]["Debarment_Risk"]
        elig_lbl = res["linguistic_labels"]["Exam_Eligibility"]

        self.att_result_text.delete('1.0', tk.END)
        self.att_result_text.insert(tk.END, "====================================================================\n")
        self.att_result_text.insert(tk.END, "BAHRIA UNIVERSITY ATTENDANCE & EXAM ADVISORY (SECTION 1.27)\n")
        self.att_result_text.insert(tk.END, f"Recorded Attendance: {att:.1f}% | Makeup Tutorial Credit: {tut:.1f}/10\n")
        self.att_result_text.insert(tk.END, "--------------------------------------------------------------------\n")
        self.att_result_text.insert(tk.END, f"CRISP DEBARMENT RISK INDEX: {risk:.2f} / 100 --> [{risk_lbl.replace('_', ' ')}]\n")
        self.att_result_text.insert(tk.END, f"CRISP EXAM ELIGIBILITY:     {elig:.2f} / 100 --> [{elig_lbl.replace('_', ' ')}]\n")
        self.att_result_text.insert(tk.END, "--------------------------------------------------------------------\n")
        self.att_result_text.insert(tk.END, "POLICY VERDICT (HANDBOOK CLAUSE TRACE):\n")
        if att < 75.0 and tut < 4.0:
            self.att_result_text.insert(tk.END, "DEBARRED FROM FINAL EXAMINATION.\n")
            self.att_result_text.insert(tk.END, "Handbook Sec 1.27.1: Students must attend at least 75% of contact hours.\n")
            self.att_result_text.insert(tk.END, "Strict policy: 'On no account, any shortfall in attendance shall be condoned.'\n")
        elif att < 75.0 and tut >= 6.0:
            self.att_result_text.insert(tk.END, "CONDITIONAL ELIGIBILITY VIA APPROVED MAKEUP TUTORIALS.\n")
            self.att_result_text.insert(tk.END, "Handbook Sec 1.27.2: Official BUHO approved sports/activity tutorials held;\n")
            self.att_result_text.insert(tk.END, "Attendance credited to student record to meet the 75% mandate.\n")
        else:
            self.att_result_text.insert(tk.END, "ELIGIBLE TO SIT IN FINAL EXAMINATION.\n")
            self.att_result_text.insert(tk.END, "Attendance satisfies mandatory threshold. No debarment risk.\n")

        self.att_result_text.insert(tk.END, "\nFIRED FUZZY RULES (With Activation Strengths):\n")
        for r in res["fired_rules"]:
            self.att_result_text.insert(tk.END, f" - [{r['rule_id']}] α = {r['strength']:.3f} | {r['description']}\n")

    # =========================================================================
    # TAB 3: Course Withdrawal & Fee Adjustment
    # =========================================================================
    def _setup_withdrawal_tab(self):
        pane = ttk.PanedWindow(self.tab_withdrawal, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.LabelFrame(pane, text="Course Withdrawal Timing Inputs", padding=15)
        pane.add(left_frame, weight=1)

        ttk.Label(left_frame, text="Days Elapsed Since Semester Start (Day 1 - 70):").pack(anchor=tk.W, pady=(0, 2))
        self.wdl_days_var = tk.DoubleVar(value=10.0)
        ttk.Scale(left_frame, from_=1.0, to=70.0, variable=self.wdl_days_var, orient=tk.HORIZONTAL,
                  command=lambda v: self.wdl_entry.delete(0, tk.END) or self.wdl_entry.insert(0, f"{float(v):.0f}")).pack(fill=tk.X)
        self.wdl_entry = ttk.Entry(left_frame, width=8)
        self.wdl_entry.insert(0, "10")
        self.wdl_entry.pack(anchor=tk.W, pady=(2, 10))

        ttk.Label(left_frame, text="Quick Timeline Selectors:", font=('Segoe UI', 9, 'bold')).pack(anchor=tk.W, pady=(5, 2))
        quick_btn_frame = ttk.Frame(left_frame)
        quick_btn_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Button(quick_btn_frame, text="Day 4 (Wk 1)", command=lambda: self._set_wdl_day(4)).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_btn_frame, text="Day 12 (Wk 2)", command=lambda: self._set_wdl_day(12)).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_btn_frame, text="Day 30 (Wk 5)", command=lambda: self._set_wdl_day(30)).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_btn_frame, text="Day 55 (Wk 8)", command=lambda: self._set_wdl_day(55)).pack(side=tk.LEFT, padx=2)

        calc_btn = ttk.Button(left_frame, text="Evaluate Withdrawal Consequences", style="Accent.TButton", command=self.eval_withdrawal)
        calc_btn.pack(fill=tk.X, pady=8)

        right_frame = ttk.LabelFrame(pane, text="Transcript Impact & Fee Adjustment Outcome", padding=15)
        pane.add(right_frame, weight=2)

        self.wdl_result_text = tk.Text(right_frame, wrap=tk.WORD, font=('Consolas', 10), height=18)
        self.wdl_result_text.pack(fill=tk.BOTH, expand=True)

        self.eval_withdrawal()

    def _set_wdl_day(self, day):
        self.wdl_entry.delete(0, tk.END)
        self.wdl_entry.insert(0, str(day))
        self.wdl_days_var.set(day)
        self.eval_withdrawal()

    def eval_withdrawal(self):
        try:
            day = float(self.wdl_entry.get())
        except ValueError:
            day = self.wdl_days_var.get()

        res = self.wdl_sys.infer({"Withdrawal_Day": day})
        pen = res["crisp_outputs"]["Transcript_Penalty_Severity"]
        ref = res["crisp_outputs"]["Fee_Refund_Adjustment_Pct"]
        pen_lbl = res["linguistic_labels"]["Transcript_Penalty_Severity"]
        ref_lbl = res["linguistic_labels"]["Fee_Refund_Adjustment_Pct"]

        week_num = int((day - 1) // 7) + 1

        self.wdl_result_text.delete('1.0', tk.END)
        self.wdl_result_text.insert(tk.END, "====================================================================\n")
        self.wdl_result_text.insert(tk.END, "BAHRIA UNIVERSITY WITHDRAWAL & REFUND ADVISORY (SECTION 1.14)\n")
        self.wdl_result_text.insert(tk.END, f"Withdrawal Application Day: {day:.0f} (Semester Week {week_num})\n")
        self.wdl_result_text.insert(tk.END, "--------------------------------------------------------------------\n")
        self.wdl_result_text.insert(tk.END, f"CRISP TRANSCRIPT PENALTY:   {pen:.2f} / 100 --> [{pen_lbl.replace('_', ' ')}]\n")
        self.wdl_result_text.insert(tk.END, f"CRISP FEE ADJUSTMENT / REF: {ref:.2f} %     --> [{ref_lbl.replace('_', ' ')}]\n")
        self.wdl_result_text.insert(tk.END, "--------------------------------------------------------------------\n")
        self.wdl_result_text.insert(tk.END, "POLICY TIMELINE ANALYSIS:\n")
        if day <= 7:
            self.wdl_result_text.insert(tk.END, "- Transcript: NOT RECORDED on transcript (Sec 1.14.2)\n")
            self.wdl_result_text.insert(tk.END, "- Fee: 100% FULL FEE ADJUSTED/transferred to next semester (Sec 1.14.4)\n")
        elif day <= 15:
            self.wdl_result_text.insert(tk.END, "- Transcript: NOT RECORDED on transcript (Within first 2 weeks, Sec 1.14.2)\n")
            self.wdl_result_text.insert(tk.END, "- Fee: 50% HALF FEE ADJUSTED (Within 15 days, Sec 1.14.4)\n")
        elif day <= 49:
            self.wdl_result_text.insert(tk.END, "- Transcript: RECORDED WITH 'W' GRADE on transcript (Sec 1.14.3)\n")
            self.wdl_result_text.insert(tk.END, "- Fee: NO FEE ADJUSTMENT (Withdrawn after Day 15, Sec 1.14.4)\n")
        else:
            self.wdl_result_text.insert(tk.END, "- Transcript: WITHDRAWAL NOT ALLOWED! (After Week 7, Sec 1.14.3)\n")
            self.wdl_result_text.insert(tk.END, "- Consequence: Student must remain enrolled; unattempted course defaults to 'F'.\n")
            self.wdl_result_text.insert(tk.END, "- Fee: NO FEE ADJUSTMENT OR REFUND.\n")

        self.wdl_result_text.insert(tk.END, "\nFIRED FUZZY RULES (With Activation Strengths):\n")
        for r in res["fired_rules"]:
            self.wdl_result_text.insert(tk.END, f" - [{r['rule_id']}] α = {r['strength']:.3f} | {r['description']}\n")

    # =========================================================================
    # TAB 4: Course Repeat Subsystem
    # =========================================================================
    def _setup_repeat_tab(self):
        pane = ttk.PanedWindow(self.tab_repeat, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.LabelFrame(pane, text="Course Repeat Prerequisites", padding=15)
        pane.add(left_frame, weight=1)

        ttk.Label(left_frame, text="Previously Obtained Grade Point (GP 0.0 - 4.0):").pack(anchor=tk.W, pady=(0, 2))
        self.rep_grade_var = tk.DoubleVar(value=2.0)
        ttk.Scale(left_frame, from_=0.0, to=4.0, variable=self.rep_grade_var, orient=tk.HORIZONTAL,
                  command=lambda v: self.rep_grade_entry.delete(0, tk.END) or self.rep_grade_entry.insert(0, f"{float(v):.2f}")).pack(fill=tk.X)
        self.rep_grade_entry = ttk.Entry(left_frame, width=8)
        self.rep_grade_entry.insert(0, "2.00")
        self.rep_grade_entry.pack(anchor=tk.W, pady=(2, 10))

        ttk.Label(left_frame, text="Class Enrollment Strength (Registered Students):").pack(anchor=tk.W, pady=(0, 2))
        self.rep_size_var = tk.IntVar(value=14)
        ttk.Scale(left_frame, from_=1, to=30, variable=self.rep_size_var, orient=tk.HORIZONTAL,
                  command=lambda v: self.rep_size_entry.delete(0, tk.END) or self.rep_size_entry.insert(0, f"{int(float(v))}")).pack(fill=tk.X)
        self.rep_size_entry = ttk.Entry(left_frame, width=8)
        self.rep_size_entry.insert(0, "14")
        self.rep_size_entry.pack(anchor=tk.W, pady=(2, 15))

        calc_btn = ttk.Button(left_frame, text="Evaluate Repeat Feasibility", style="Accent.TButton", command=self.eval_repeat)
        calc_btn.pack(fill=tk.X, pady=8)

        right_frame = ttk.LabelFrame(pane, text="Repeat Approval Index & CGPA Recovery Potential", padding=15)
        pane.add(right_frame, weight=2)

        self.rep_result_text = tk.Text(right_frame, wrap=tk.WORD, font=('Consolas', 10), height=18)
        self.rep_result_text.pack(fill=tk.BOTH, expand=True)

        self.eval_repeat()

    def eval_repeat(self):
        try:
            gp = float(self.rep_grade_entry.get())
        except ValueError:
            gp = self.rep_grade_var.get()
        try:
            size = float(self.rep_size_entry.get())
        except ValueError:
            size = float(self.rep_size_var.get())

        res = self.rep_sys.infer({"Earned_Course_GPA": gp, "Cohort_Enrolled_Size": size})
        perm = res["crisp_outputs"]["Repeat_Permission_Index"]
        gain = res["crisp_outputs"]["CGPA_Improvement_Impact"]
        perm_lbl = res["linguistic_labels"]["Repeat_Permission_Index"]
        gain_lbl = res["linguistic_labels"]["CGPA_Improvement_Impact"]

        self.rep_result_text.delete('1.0', tk.END)
        self.rep_result_text.insert(tk.END, "====================================================================\n")
        self.rep_result_text.insert(tk.END, "BAHRIA UNIVERSITY COURSE REPEAT ADVISORY (SECTION 1.17)\n")
        self.rep_result_text.insert(tk.END, f"Prior Course Grade Point: {gp:.2f} | Enrolled Class Size: {int(size)} students\n")
        self.rep_result_text.insert(tk.END, "--------------------------------------------------------------------\n")
        self.rep_result_text.insert(tk.END, f"CRISP REPEAT PERMISSION INDEX: {perm:.2f} / 100 --> [{perm_lbl.replace('_', ' ')}]\n")
        self.rep_result_text.insert(tk.END, f"CRISP CGPA RECOVERY IMPACT:    {gain:.2f} / 100 --> [{gain_lbl.replace('_', ' ')}]\n")
        self.rep_result_text.insert(tk.END, "--------------------------------------------------------------------\n")
        self.rep_result_text.insert(tk.END, "POLICY CHECK & HOD RECOMMENDATION:\n")
        if gp > 2.5:
            self.rep_result_text.insert(tk.END, "INELIGIBLE TO REPEAT COURSE.\n")
            self.rep_result_text.insert(tk.END, "Handbook Sec 1.17.1: Students may only repeat courses with grade 'C+' (GP 2.5) or less.\n")
        elif size < 10:
            self.rep_result_text.insert(tk.END, "ELIGIBLE BUT QUORUM NOT MET.\n")
            self.rep_result_text.insert(tk.END, f"Current enrollment is {int(size)} students. Handbook Sec 1.17.2 states running the\n")
            self.rep_result_text.insert(tk.END, "course is contingent on meeting the minimum class strength of TEN (10) students.\n")
        else:
            self.rep_result_text.insert(tk.END, "APPROVED FOR REPETITION.\n")
            self.rep_result_text.insert(tk.END, "Handbook Sec 1.17.1 & 1.17.2: Grade is <= 2.5 and class quorum (>=10) is satisfied.\n")
            self.rep_result_text.insert(tk.END, "Note: Highest grade achieved will be counted towards CGPA; all attempts show on transcript.\n")

        self.rep_result_text.insert(tk.END, "\nFIRED FUZZY RULES (With Activation Strengths):\n")
        for r in res["fired_rules"]:
            self.rep_result_text.insert(tk.END, f" - [{r['rule_id']}] α = {r['strength']:.3f} | {r['description']}\n")

    # =========================================================================
    # TAB 5: Unified Student Profile
    # =========================================================================
    def _setup_unified_tab(self):
        frame = ttk.Frame(self.tab_unified, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)

        top_box = ttk.LabelFrame(frame, text="Unified Student Scenario Parameters", padding=10)
        top_box.pack(fill=tk.X, pady=(0, 10))

        r1 = ttk.Frame(top_box)
        r1.pack(fill=tk.X, pady=4)
        ttk.Label(r1, text="Degree Program:", width=18).pack(side=tk.LEFT)
        self.u_prog = ttk.Combobox(r1, values=list(PROGRAM_MIN_CGPA.keys()), state="readonly", width=22)
        self.u_prog.set("BS / BBA / BEE")
        self.u_prog.pack(side=tk.LEFT, padx=5)

        ttk.Label(r1, text="Cumulative GPA:", width=16).pack(side=tk.LEFT, padx=(20, 0))
        self.u_cgpa = ttk.Entry(r1, width=8)
        self.u_cgpa.insert(0, "1.92")
        self.u_cgpa.pack(side=tk.LEFT, padx=5)

        ttk.Label(r1, text="Consecutive Probations:", width=22).pack(side=tk.LEFT, padx=(20, 0))
        self.u_prob = ttk.Combobox(r1, values=["0", "1", "2"], state="readonly", width=5)
        self.u_prob.set("1")
        self.u_prob.pack(side=tk.LEFT, padx=5)

        r2 = ttk.Frame(top_box)
        r2.pack(fill=tk.X, pady=4)
        ttk.Label(r2, text="Attendance Pct (%):", width=18).pack(side=tk.LEFT)
        self.u_att = ttk.Entry(r2, width=8)
        self.u_att.insert(0, "73.5")
        self.u_att.pack(side=tk.LEFT, padx=5)

        ttk.Label(r2, text="Makeup Tutorials (0-10):", width=22).pack(side=tk.LEFT, padx=(20, 0))
        self.u_tut = ttk.Entry(r2, width=8)
        self.u_tut.insert(0, "2.0")
        self.u_tut.pack(side=tk.LEFT, padx=5)

        ttk.Label(r2, text="Repeat Target Grade (GP):", width=24).pack(side=tk.LEFT, padx=(20, 0))
        self.u_rep_gp = ttk.Entry(r2, width=8)
        self.u_rep_gp.insert(0, "1.67")
        self.u_rep_gp.pack(side=tk.LEFT, padx=5)

        r3 = ttk.Frame(top_box)
        r3.pack(fill=tk.X, pady=4)
        ttk.Label(r3, text="Withdrawal Day (1-70):", width=18).pack(side=tk.LEFT)
        self.u_wdl_day = ttk.Entry(r3, width=8)
        self.u_wdl_day.insert(0, "12")
        self.u_wdl_day.pack(side=tk.LEFT, padx=5)

        ttk.Label(r3, text="Repeat Class Size:", width=22).pack(side=tk.LEFT, padx=(20, 0))
        self.u_rep_size = ttk.Entry(r3, width=8)
        self.u_rep_size.insert(0, "15")
        self.u_rep_size.pack(side=tk.LEFT, padx=5)

        u_btn = ttk.Button(r3, text="Run 360 Comprehensive Student Diagnostic", style="Accent.TButton", command=self.eval_unified)
        u_btn.pack(side=tk.LEFT, padx=(30, 0))

        self.u_text = tk.Text(frame, wrap=tk.WORD, font=('Consolas', 10), height=18)
        self.u_text.pack(fill=tk.BOTH, expand=True)

        self.eval_unified()

    def eval_unified(self):
        try:
            cgpa = float(self.u_cgpa.get())
            prog = self.u_prog.get()
            min_gpa = PROGRAM_MIN_CGPA.get(prog, 2.00)
            consec = float(self.u_prob.get())
            margin = round(cgpa - min_gpa, 2)
            att = float(self.u_att.get())
            tut = float(self.u_tut.get())
            rep_gp = float(self.u_rep_gp.get())
            rep_size = float(self.u_rep_size.get())
            wdl_day = float(self.u_wdl_day.get())
        except Exception as e:
            messagebox.showerror("Input Error", f"Please check input values: {e}")
            return

        res_prb = self.prb_sys.infer({"CGPA_Margin": margin, "Consecutive_Probations": consec})
        res_att = self.att_sys.infer({"Attendance_Pct": att, "Remedial_Makeup_Score": tut})
        res_rep = self.rep_sys.infer({"Earned_Course_GPA": rep_gp, "Cohort_Enrolled_Size": rep_size})
        res_wdl = self.wdl_sys.infer({"Withdrawal_Day": wdl_day})

        self.u_text.delete('1.0', tk.END)
        self.u_text.insert(tk.END, "====================================================================================\n")
        self.u_text.insert(tk.END, "       BAHRIA UNIVERSITY - 360 DEGREE INTEGRATED STUDENT ADVISORY REPORT\n")
        self.u_text.insert(tk.END, "====================================================================================\n\n")

        self.u_text.insert(tk.END, f"[DOMAIN 1: ACADEMIC STANDING & PROBATION STATUS (SECTION 5.5)]\n")
        self.u_text.insert(tk.END, f"  * Program: {prog} (Minimum CGPA: {min_gpa:.2f}) | Current CGPA: {cgpa:.2f} (Delta: {margin:+.2f})\n")
        self.u_text.insert(tk.END, f"  * Academic Risk Score: {res_prb['crisp_outputs']['Academic_Risk_Severity']:.1f}/100 [{res_prb['linguistic_labels']['Academic_Risk_Severity']}]\n")
        self.u_text.insert(tk.END, f"  * Registration Action: {res_prb['crisp_outputs']['Registration_Action_Advisory']:.1f}/100 [{res_prb['linguistic_labels']['Registration_Action_Advisory']}]\n\n")

        self.u_text.insert(tk.END, f"[DOMAIN 2: ATTENDANCE & EXAMINATION ELIGIBILITY (SECTION 1.27)]\n")
        self.u_text.insert(tk.END, f"  * Attendance Recorded: {att:.1f}% | Approved Remedial Credit: {tut:.1f}/10\n")
        self.u_text.insert(tk.END, f"  * Debarment Risk Index: {res_att['crisp_outputs']['Debarment_Risk']:.1f}/100 [{res_att['linguistic_labels']['Debarment_Risk']}]\n")
        self.u_text.insert(tk.END, f"  * Exam Eligibility:     {res_att['crisp_outputs']['Exam_Eligibility']:.1f}/100 [{res_att['linguistic_labels']['Exam_Eligibility']}]\n\n")

        self.u_text.insert(tk.END, f"[DOMAIN 3: COURSE WITHDRAWAL & FINANCIAL TIMELINE (SECTION 1.14)]\n")
        self.u_text.insert(tk.END, f"  * Application on Day {wdl_day:.0f} (Week {int((wdl_day-1)//7)+1})\n")
        self.u_text.insert(tk.END, f"  * Transcript Impact:    {res_wdl['crisp_outputs']['Transcript_Penalty_Severity']:.1f}/100 [{res_wdl['linguistic_labels']['Transcript_Penalty_Severity']}]\n")
        self.u_text.insert(tk.END, f"  * Fee Refund/Transfer:  {res_wdl['crisp_outputs']['Fee_Refund_Adjustment_Pct']:.1f}% [{res_wdl['linguistic_labels']['Fee_Refund_Adjustment_Pct']}]\n\n")

        self.u_text.insert(tk.END, f"[DOMAIN 4: COURSE REPEAT & GRADE IMPROVEMENT (SECTION 1.17)]\n")
        self.u_text.insert(tk.END, f"  * Course Grade: {rep_gp:.2f} GP | Registered Class Size: {int(rep_size)} students\n")
        self.u_text.insert(tk.END, f"  * Repeat Permission:    {res_rep['crisp_outputs']['Repeat_Permission_Index']:.1f}/100 [{res_rep['linguistic_labels']['Repeat_Permission_Index']}]\n")
        self.u_text.insert(tk.END, f"  * CGPA Recovery Impact: {res_rep['crisp_outputs']['CGPA_Improvement_Impact']:.1f}/100 [{res_rep['linguistic_labels']['CGPA_Improvement_Impact']}]\n\n")

        self.u_text.insert(tk.END, "====================================================================================\n")
        self.u_text.insert(tk.END, "SYNTHESIZED ADVISORY RECOMMENDATIONS FOR ACADEMIC COUNSELOR:\n")
        if res_prb['crisp_outputs']['Academic_Risk_Severity'] > 75:
            self.u_text.insert(tk.END, "(!) URGENT: Student is on the verge of being dropped. Prioritize repeating deficient courses\n")
            self.u_text.insert(tk.END, "    and seek immediate Principal approval for semester registration.\n")
        if res_att['crisp_outputs']['Exam_Eligibility'] < 35:
            self.u_text.insert(tk.END, "(!) CRITICAL: Student is debarred from final exam in the course due to attendance shortfall.\n")
            self.u_text.insert(tk.END, "    Schedule makeup tutorials if an official BUHO extracurricular clash was approved.\n")
        if rep_gp <= 2.5 and rep_size >= 10:
            self.u_text.insert(tk.END, "(*) RECOVERY PATHWAY: Repeating the course with GP <= 2.5 is highly recommended to\n")
            self.u_text.insert(tk.END, "    remedy the low CGPA and lift the academic probation status.\n")


def main():
    if "--cli" in sys.argv:
        print("Running in CLI mode. Please execute test_suite.py for automated verification.")
        return
    root = tk.Tk()
    app = FuzzyAdvisorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
