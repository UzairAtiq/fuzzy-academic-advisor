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
Comprehensive Test Suite and Evaluation Harness for Bahria University FIS
Contains 34 distinct test queries covering:
- Normal Cases (typical scenarios)
- Boundary Cases (75% attendance, 2.0/2.5/3.0 CGPA, Day 7/15/49, Grade 2.5, Quorum 10)
- Out-of-Range and Invalid Cases (-10%, 120%, CGPA 4.8, Day 120)
Generates evaluation tables, accuracy statistics, and failure analysis.
"""

import json
from typing import List, Dict, Any
from models import (build_attendance_subsystem, build_withdrawal_subsystem,
                    build_repeat_subsystem, build_probation_subsystem)

# Initialize engines
att_sys = build_attendance_subsystem()
wdl_sys = build_withdrawal_subsystem()
rep_sys = build_repeat_subsystem()
prb_sys = build_probation_subsystem()

TEST_CASES: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # DOMAIN 1: CLASS ATTENDANCE & EXAM ELIGIBILITY (SECTION 1.27)
    # -------------------------------------------------------------------------
    {
        "id": "TC_ATT_01",
        "domain": "Attendance (1.27)",
        "type": "Normal",
        "inputs": {"Attendance_Pct": 88.0, "Remedial_Makeup_Score": 0.0},
        "description": "Regular BS student with 88% attendance and no makeup tutorials.",
        "expected_handbook": "Eligible for final exam; Safe attendance (>= 75%).",
        "target_subsystem": att_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Debarment_Risk"] == "Safe" and res["linguistic_labels"]["Exam_Eligibility"] == "Fully_Eligible"
    },
    {
        "id": "TC_ATT_02",
        "domain": "Attendance (1.27)",
        "type": "Normal",
        "inputs": {"Attendance_Pct": 55.0, "Remedial_Makeup_Score": 0.0},
        "description": "Severely deficient student with 55% attendance and no makeup.",
        "expected_handbook": "Debarred from final examination; no condoning allowed.",
        "target_subsystem": att_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Debarment_Risk"] in ["Barred_Critical", "High_Risk"] and res["linguistic_labels"]["Exam_Eligibility"] == "Ineligible_Barred"
    },
    {
        "id": "TC_ATT_03",
        "domain": "Attendance (1.27)",
        "type": "Boundary",
        "inputs": {"Attendance_Pct": 75.0, "Remedial_Makeup_Score": 0.0},
        "description": "Exact threshold boundary: Attendance = 75.0%.",
        "expected_handbook": "Eligible for final exam; minimum 75% met exactly.",
        "target_subsystem": att_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Exam_Eligibility"] >= 50.0 # Boundary transition
    },
    {
        "id": "TC_ATT_04",
        "domain": "Attendance (1.27)",
        "type": "Boundary",
        "inputs": {"Attendance_Pct": 74.5, "Remedial_Makeup_Score": 0.0},
        "description": "Just below threshold: Attendance = 74.5% (shortfall of 0.5%).",
        "expected_handbook": "Debarred; shortfall cannot be condoned under Section 1.27.1.",
        "target_subsystem": att_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Debarment_Risk"] > 50.0 and res["linguistic_labels"]["Exam_Eligibility"] in ["Ineligible_Barred", "Conditional_Tutorial"]
    },
    {
        "id": "TC_ATT_05",
        "domain": "Attendance (1.27)",
        "type": "Boundary",
        "inputs": {"Attendance_Pct": 75.5, "Remedial_Makeup_Score": 0.0},
        "description": "Just above threshold: Attendance = 75.5%.",
        "expected_handbook": "Eligible; meets minimum 75% contact hours.",
        "target_subsystem": att_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Exam_Eligibility"] >= 55.0
    },
    {
        "id": "TC_ATT_06",
        "domain": "Attendance (1.27)",
        "type": "Normal (Exception)",
        "inputs": {"Attendance_Pct": 68.0, "Remedial_Makeup_Score": 9.0},
        "description": "Student at 68% attendance but has BUHO-approved sports tutorials (Sec 1.27.2).",
        "expected_handbook": "Conditional / Eligible once makeup tutorials are credited to record.",
        "target_subsystem": att_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Exam_Eligibility"] in ["Conditional_Tutorial", "Fully_Eligible"]
    },
    {
        "id": "TC_ATT_07",
        "domain": "Attendance (1.27)",
        "type": "Invalid / Out-of-Range",
        "inputs": {"Attendance_Pct": -15.0, "Remedial_Makeup_Score": 0.0},
        "description": "Negative attendance value (-15%) entered due to sensor error.",
        "expected_handbook": "Invalid input; should clamp to 0.0% and evaluate as Barred.",
        "target_subsystem": att_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Debarment_Risk"] == "Barred_Critical"
    },
    {
        "id": "TC_ATT_08",
        "domain": "Attendance (1.27)",
        "type": "Invalid / Out-of-Range",
        "inputs": {"Attendance_Pct": 135.0, "Remedial_Makeup_Score": 0.0},
        "description": "Attendance exceeding 100% (135%) entered erroneously.",
        "expected_handbook": "Invalid input; should clamp to 100.0% and evaluate as Safe/Exemplary.",
        "target_subsystem": att_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Debarment_Risk"] == "Safe"
    },

    # -------------------------------------------------------------------------
    # DOMAIN 2: COURSE WITHDRAWAL & FEE ADJUSTMENT (SECTION 1.14)
    # -------------------------------------------------------------------------
    {
        "id": "TC_WDL_01",
        "domain": "Withdrawal (1.14)",
        "type": "Normal",
        "inputs": {"Withdrawal_Day": 4.0},
        "description": "Student withdraws on Day 4 (Week 1).",
        "expected_handbook": "No record on transcript (Sec 1.14.2) and 100% full fee adjustment (Sec 1.14.4).",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Transcript_Penalty_Severity"] == "Clean_No_Record" and res["linguistic_labels"]["Fee_Refund_Adjustment_Pct"] == "Full_Adjustment_100Pct"
    },
    {
        "id": "TC_WDL_02",
        "domain": "Withdrawal (1.14)",
        "type": "Normal",
        "inputs": {"Withdrawal_Day": 11.0},
        "description": "Student withdraws on Day 11 (Week 2, within 15 days).",
        "expected_handbook": "No record on transcript (Sec 1.14.2) and 50% fee adjustment (Sec 1.14.4).",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Transcript_Penalty_Severity"] == "Clean_No_Record" and res["linguistic_labels"]["Fee_Refund_Adjustment_Pct"] == "Half_Adjustment_50Pct"
    },
    {
        "id": "TC_WDL_03",
        "domain": "Withdrawal (1.14)",
        "type": "Normal",
        "inputs": {"Withdrawal_Day": 32.0},
        "description": "Student withdraws on Day 32 (Week 5).",
        "expected_handbook": "Recorded as 'W' grade on transcript (Sec 1.14.3); No fee adjustment (Sec 1.14.4).",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Transcript_Penalty_Severity"] == "Recorded_W_Grade" and res["linguistic_labels"]["Fee_Refund_Adjustment_Pct"] == "No_Adjustment"
    },
    {
        "id": "TC_WDL_04",
        "domain": "Withdrawal (1.14)",
        "type": "Normal",
        "inputs": {"Withdrawal_Day": 58.0},
        "description": "Student attempts to withdraw on Day 58 (Week 9, post Week 7).",
        "expected_handbook": "Withdrawal disallowed (Sec 1.14.3); No fee adjustment.",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Transcript_Penalty_Severity"] == "Disallowed_Withdrawal" and res["linguistic_labels"]["Fee_Refund_Adjustment_Pct"] == "No_Adjustment"
    },
    {
        "id": "TC_WDL_05",
        "domain": "Withdrawal (1.14)",
        "type": "Boundary",
        "inputs": {"Withdrawal_Day": 7.0},
        "description": "Exact Day 7 boundary (End of Week 1).",
        "expected_handbook": "Full fee adjustment and clean record.",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Fee_Refund_Adjustment_Pct"] >= 70.0
    },
    {
        "id": "TC_WDL_06",
        "domain": "Withdrawal (1.14)",
        "type": "Boundary",
        "inputs": {"Withdrawal_Day": 8.0},
        "description": "Day 8 (Just into Week 2).",
        "expected_handbook": "Clean record on transcript; Half fee adjustment.",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Transcript_Penalty_Severity"] < 30.0 and res["crisp_outputs"]["Fee_Refund_Adjustment_Pct"] < 80.0
    },
    {
        "id": "TC_WDL_07",
        "domain": "Withdrawal (1.14)",
        "type": "Boundary",
        "inputs": {"Withdrawal_Day": 15.0},
        "description": "Exact Day 15 boundary (Last day for 50% fee adjustment).",
        "expected_handbook": "Half fee adjustment; Clean record (end of week 2).",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Fee_Refund_Adjustment_Pct"] >= 40.0
    },
    {
        "id": "TC_WDL_08",
        "domain": "Withdrawal (1.14)",
        "type": "Boundary",
        "inputs": {"Withdrawal_Day": 16.0},
        "description": "Day 16 (First day of Week 3, post day 15).",
        "expected_handbook": "'W' grade on transcript; Zero fee adjustment.",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Fee_Refund_Adjustment_Pct"] <= 30.0 and res["crisp_outputs"]["Transcript_Penalty_Severity"] >= 35.0
    },
    {
        "id": "TC_WDL_09",
        "domain": "Withdrawal (1.14)",
        "type": "Boundary",
        "inputs": {"Withdrawal_Day": 49.0},
        "description": "Exact Day 49 boundary (End of Week 7, final day to withdraw).",
        "expected_handbook": "'W' grade allowed; last valid withdrawal day.",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Transcript_Penalty_Severity"] < 75.0
    },
    {
        "id": "TC_WDL_10",
        "domain": "Withdrawal (1.14)",
        "type": "Boundary",
        "inputs": {"Withdrawal_Day": 50.0},
        "description": "Day 50 (Start of Week 8, post Week 7 cutoff).",
        "expected_handbook": "Withdrawal disallowed under Section 1.14.3.",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Transcript_Penalty_Severity"] >= 70.0
    },
    {
        "id": "TC_WDL_11",
        "domain": "Withdrawal (1.14)",
        "type": "Invalid / Out-of-Range",
        "inputs": {"Withdrawal_Day": -5.0},
        "description": "Negative timeline input (-5 days).",
        "expected_handbook": "Invalid; clamp to Day 0 (Clean record, full fee adjustment).",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Transcript_Penalty_Severity"] == "Clean_No_Record"
    },
    {
        "id": "TC_WDL_12",
        "domain": "Withdrawal (1.14)",
        "type": "Invalid / Out-of-Range",
        "inputs": {"Withdrawal_Day": 120.0},
        "description": "Days far beyond semester end (120 days).",
        "expected_handbook": "Invalid/Excessive; clamp to max day (Disallowed, zero refund).",
        "target_subsystem": wdl_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Transcript_Penalty_Severity"] == "Disallowed_Withdrawal"
    },

    # -------------------------------------------------------------------------
    # DOMAIN 3: REPEATING A COURSE (SECTION 1.17)
    # -------------------------------------------------------------------------
    {
        "id": "TC_REP_01",
        "domain": "Course Repeat (1.17)",
        "type": "Normal",
        "inputs": {"Earned_Course_GPA": 1.0, "Cohort_Enrolled_Size": 16.0},
        "description": "Grade 'D' (GP 1.0) and class size 16 (quorum met).",
        "expected_handbook": "Approved to repeat (Sec 1.17.1); high CGPA recovery potential.",
        "target_subsystem": rep_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Repeat_Permission_Index"] == "Approved_Permitted" and res["linguistic_labels"]["CGPA_Improvement_Impact"] == "Maximum_Recovery"
    },
    {
        "id": "TC_REP_02",
        "domain": "Course Repeat (1.17)",
        "type": "Normal",
        "inputs": {"Earned_Course_GPA": 2.33, "Cohort_Enrolled_Size": 14.0},
        "description": "Grade 'C+' (GP 2.33) and class size 14.",
        "expected_handbook": "Approved to repeat (Grade <= 2.5 and quorum >= 10 satisfied).",
        "target_subsystem": rep_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Repeat_Permission_Index"] == "Approved_Permitted"
    },
    {
        "id": "TC_REP_03",
        "domain": "Course Repeat (1.17)",
        "type": "Normal",
        "inputs": {"Earned_Course_GPA": 3.0, "Cohort_Enrolled_Size": 20.0},
        "description": "Grade 'B' (GP 3.0) and class size 20.",
        "expected_handbook": "Denied; cannot repeat grade above C+ (2.5 GP) under Sec 1.17.1.",
        "target_subsystem": rep_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Repeat_Permission_Index"] == "Denied_Ineligible"
    },
    {
        "id": "TC_REP_04",
        "domain": "Course Repeat (1.17)",
        "type": "Normal (Quorum Deficit)",
        "inputs": {"Earned_Course_GPA": 1.33, "Cohort_Enrolled_Size": 5.0},
        "description": "Grade 'D+' (GP 1.33) but class size is only 5 (< 10 quorum).",
        "expected_handbook": "Conditional / Pending; eligible grade but under-enrolled under Sec 1.17.2.",
        "target_subsystem": rep_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Repeat_Permission_Index"] == "Conditional_Quorum_Pending"
    },
    {
        "id": "TC_REP_05",
        "domain": "Course Repeat (1.17)",
        "type": "Boundary",
        "inputs": {"Earned_Course_GPA": 2.50, "Cohort_Enrolled_Size": 12.0},
        "description": "Exact Grade Point threshold boundary: GP = 2.50 (C+ cap).",
        "expected_handbook": "Eligible to repeat (Sec 1.17.1 specifies 'C+ or less').",
        "target_subsystem": rep_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Repeat_Permission_Index"] >= 50.0
    },
    {
        "id": "TC_REP_06",
        "domain": "Course Repeat (1.17)",
        "type": "Boundary",
        "inputs": {"Earned_Course_GPA": 2.55, "Cohort_Enrolled_Size": 12.0},
        "description": "Just above Grade Point threshold: GP = 2.55.",
        "expected_handbook": "Ineligible / Denied (exceeds 2.5 C+ cap).",
        "target_subsystem": rep_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Repeat_Permission_Index"] < 65.0
    },
    {
        "id": "TC_REP_07",
        "domain": "Course Repeat (1.17)",
        "type": "Boundary",
        "inputs": {"Earned_Course_GPA": 1.70, "Cohort_Enrolled_Size": 10.0},
        "description": "Exact Class Size Quorum threshold: Size = 10 students.",
        "expected_handbook": "Approved to run; minimum class strength of 10 met exactly (Sec 1.17.2).",
        "target_subsystem": rep_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Repeat_Permission_Index"] >= 65.0
    },
    {
        "id": "TC_REP_08",
        "domain": "Course Repeat (1.17)",
        "type": "Boundary",
        "inputs": {"Earned_Course_GPA": 1.70, "Cohort_Enrolled_Size": 9.0},
        "description": "Class size just below quorum: Size = 9 students.",
        "expected_handbook": "Conditional; fails minimum 10 students quorum.",
        "target_subsystem": rep_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Repeat_Permission_Index"] < 70.0
    },
    {
        "id": "TC_REP_09",
        "domain": "Course Repeat (1.17)",
        "type": "Invalid / Out-of-Range",
        "inputs": {"Earned_Course_GPA": 4.80, "Cohort_Enrolled_Size": 15.0},
        "description": "Grade point exceeding maximum (4.80 GP).",
        "expected_handbook": "Invalid grade; clamp to 4.0 and Deny repeat.",
        "target_subsystem": rep_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Repeat_Permission_Index"] == "Denied_Ineligible"
    },

    # -------------------------------------------------------------------------
    # DOMAIN 4: PROBATION & DROP RULES (SECTION 5.5)
    # -------------------------------------------------------------------------
    {
        "id": "TC_PRB_01",
        "domain": "Probation/Drop (5.5)",
        "type": "Normal",
        "inputs": {"CGPA_Margin": 0.80, "Consecutive_Probations": 0.0},
        "description": "BS Student with CGPA 2.80 (Margin +0.80) and 0 probations.",
        "expected_handbook": "Good standing; Unrestricted registration.",
        "target_subsystem": prb_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Academic_Risk_Severity"] == "Good_Standing" and res["linguistic_labels"]["Registration_Action_Advisory"] == "Unrestricted_Registration"
    },
    {
        "id": "TC_PRB_02",
        "domain": "Probation/Drop (5.5)",
        "type": "Normal",
        "inputs": {"CGPA_Margin": -0.40, "Consecutive_Probations": 0.0},
        "description": "BS Student with CGPA 1.60 (Margin -0.40) on 0 previous probations.",
        "expected_handbook": "Placed on 1st Probation; Formal warning letter by HoD (Sec 5.5.1, 5.5.2).",
        "target_subsystem": prb_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Academic_Risk_Severity"] in ["Probation_Alert", "Advisory_Warning"] and res["linguistic_labels"]["Registration_Action_Advisory"] == "Academic_Counseling_Required"
    },
    {
        "id": "TC_PRB_03",
        "domain": "Probation/Drop (5.5)",
        "type": "Normal",
        "inputs": {"CGPA_Margin": -0.25, "Consecutive_Probations": 1.0},
        "description": "Student on 1st probation fails to reach minimum (Margin -0.25).",
        "expected_handbook": "Placed on 2nd consecutive Probation; Principal approval required to register (Sec 5.5.5).",
        "target_subsystem": prb_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Academic_Risk_Severity"] in ["Probation_Alert", "Severe_Drop_Threat"]
    },
    {
        "id": "TC_PRB_04",
        "domain": "Probation/Drop (5.5)",
        "type": "Normal",
        "inputs": {"CGPA_Margin": -0.30, "Consecutive_Probations": 2.0},
        "description": "Student fails to reach minimum CGPA after 2 consecutive probations.",
        "expected_handbook": "MANDATORY DROP from academic programme (Sec 5.5.3); Registration barred.",
        "target_subsystem": prb_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Academic_Risk_Severity"] == "Severe_Drop_Threat" and res["linguistic_labels"]["Registration_Action_Advisory"] in ["Registration_Barred_Drop", "Principal_Approval_Mandatory"]
    },
    {
        "id": "TC_PRB_05",
        "domain": "Probation/Drop (5.5)",
        "type": "Normal (Reset Rule)",
        "inputs": {"CGPA_Margin": 0.15, "Consecutive_Probations": 1.0},
        "description": "Student on probation improves CGPA above minimum (Margin +0.15).",
        "expected_handbook": "Probation count RESET TO ZERO (Sec 5.5.4); Good standing restored.",
        "target_subsystem": prb_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Academic_Risk_Severity"] == "Good_Standing" and res["linguistic_labels"]["Registration_Action_Advisory"] == "Unrestricted_Registration"
    },
    {
        "id": "TC_PRB_06",
        "domain": "Probation/Drop (5.5)",
        "type": "Boundary",
        "inputs": {"CGPA_Margin": 0.00, "Consecutive_Probations": 1.0},
        "description": "Exact threshold boundary: CGPA Margin = 0.00 (CGPA exactly equals minimum).",
        "expected_handbook": "Satisfies minimum; resets probation count to zero under Sec 5.5.4.",
        "target_subsystem": prb_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Academic_Risk_Severity"] <= 50.0
    },
    {
        "id": "TC_PRB_07",
        "domain": "Probation/Drop (5.5)",
        "type": "Boundary",
        "inputs": {"CGPA_Margin": -0.02, "Consecutive_Probations": 0.0},
        "description": "Just below threshold: Margin = -0.02 (e.g. BS CGPA 1.98).",
        "expected_handbook": "Falls below minimum; placed on probation under Sec 5.5.1.",
        "target_subsystem": prb_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Academic_Risk_Severity"] >= 35.0
    },
    {
        "id": "TC_PRB_08",
        "domain": "Probation/Drop (5.5)",
        "type": "Boundary",
        "inputs": {"CGPA_Margin": +0.02, "Consecutive_Probations": 0.0},
        "description": "Just above threshold: Margin = +0.02 (e.g. BS CGPA 2.02).",
        "expected_handbook": "Meets minimum; good academic standing.",
        "target_subsystem": prb_sys,
        "eval_fn": lambda res: res["crisp_outputs"]["Academic_Risk_Severity"] <= 35.0
    },
    {
        "id": "TC_PRB_09",
        "domain": "Probation/Drop (5.5)",
        "type": "Invalid / Out-of-Range",
        "inputs": {"CGPA_Margin": -3.5, "Consecutive_Probations": 0.0},
        "description": "Extreme negative CGPA deficit (-3.5).",
        "expected_handbook": "Clamp to -2.0; triggers high risk / probation alert.",
        "target_subsystem": prb_sys,
        "eval_fn": lambda res: res["linguistic_labels"]["Academic_Risk_Severity"] in ["Probation_Alert", "Severe_Drop_Threat"]
    }
]

def run_evaluation() -> Dict[str, Any]:
    results = []
    passed = 0
    failed = 0

    for tc in TEST_CASES:
        subsystem = tc["target_subsystem"]
        res = subsystem.infer(tc["inputs"])
        is_pass = tc["eval_fn"](res)
        
        if is_pass:
            passed += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"

        results.append({
            "id": tc["id"],
            "domain": tc["domain"],
            "type": tc["type"],
            "inputs": tc["inputs"],
            "description": tc["description"],
            "expected_handbook": tc["expected_handbook"],
            "crisp_outputs": res["crisp_outputs"],
            "linguistic_labels": res["linguistic_labels"],
            "fired_rules_count": len(res["fired_rules"]),
            "status": status
        })

    total = len(TEST_CASES)
    accuracy = (passed / total) * 100.0

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "accuracy_pct": round(accuracy, 2),
        "test_results": results
    }

if __name__ == "__main__":
    report = run_evaluation()
    print("=====================================================================")
    print("      BAHRIA UNIVERSITY FIS TEST SUITE EXECUTION SUMMARY")
    print("=====================================================================")
    print(f"Total Test Queries Tested: {report['total']}")
    print(f"Passed:                   {report['passed']}")
    print(f"Failed / Divergent:       {report['failed']}")
    print(f"Overall Accuracy:         {report['accuracy_pct']} %")
    print("=====================================================================")
    
    with open("test_results.json", "w") as f:
        json.dump(report, f, indent=2)
    print("Saved complete detailed test results to 'test_results.json'.")
