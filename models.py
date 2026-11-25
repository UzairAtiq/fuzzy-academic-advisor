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
Bahria University Academic Regulations - Policy Subsystems Definitions (Calibrated)
Fine-tuned membership functions for optimal boundary behavior and clear transitional zones.
"""

from fuzzy_core import LinguisticVariable, Trimf, Trapmf, FuzzyRule, FuzzySubsystem

# ==============================================================================
# 1. Attendance & Exam Eligibility Subsystem (Section 1.27.1 - 1.27.2)
# ==============================================================================
def build_attendance_subsystem() -> FuzzySubsystem:
    att_pct = LinguisticVariable(
        name="Attendance_Pct",
        unit="%",
        universe=(0.0, 100.0),
        terms={
            "Critically_Low": Trapmf(0.0, 0.0, 60.0, 72.0),
            "Shortfall_Borderline": Trimf(68.0, 73.5, 76.5),
            "Safe_Adequate": Trimf(74.5, 82.0, 90.0),
            "Exemplary": Trapmf(86.0, 93.0, 100.0, 100.0)
        }
    )

    remedial_score = LinguisticVariable(
        name="Remedial_Makeup_Score",
        unit="scale 0-10",
        universe=(0.0, 10.0),
        terms={
            "None_Unapproved": Trapmf(0.0, 0.0, 2.0, 4.0),
            "Partial_Makeup": Trimf(3.0, 5.5, 8.0),
            "Fully_Certified": Trapmf(7.0, 9.0, 10.0, 10.0)
        }
    )

    debarment_risk = LinguisticVariable(
        name="Debarment_Risk",
        unit="index 0-100",
        universe=(0.0, 100.0),
        terms={
            "Safe": Trapmf(0.0, 0.0, 15.0, 30.0),
            "Caution_Borderline": Trimf(20.0, 38.0, 55.0),
            "High_Risk": Trimf(50.0, 70.0, 85.0),
            "Barred_Critical": Trapmf(75.0, 90.0, 100.0, 100.0)
        }
    )

    exam_eligibility = LinguisticVariable(
        name="Exam_Eligibility",
        unit="index 0-100",
        universe=(0.0, 100.0),
        terms={
            "Ineligible_Barred": Trapmf(0.0, 0.0, 20.0, 35.0),
            "Conditional_Tutorial": Trimf(30.0, 50.0, 70.0),
            "Fully_Eligible": Trapmf(65.0, 85.0, 100.0, 100.0)
        }
    )

    rules = [
        FuzzyRule("R_ATT_01", [("Attendance_Pct", "Critically_Low"), ("Remedial_Makeup_Score", "None_Unapproved")],
                  [("Debarment_Risk", "Barred_Critical"), ("Exam_Eligibility", "Ineligible_Barred")],
                  "IF Attendance is Critically Low AND Makeup is None THEN Debarment Risk is Critical Barred AND Ineligible for Final Exam (Sec 1.27.1)."),
        FuzzyRule("R_ATT_02", [("Attendance_Pct", "Critically_Low"), ("Remedial_Makeup_Score", "Partial_Makeup")],
                  [("Debarment_Risk", "High_Risk"), ("Exam_Eligibility", "Ineligible_Barred")],
                  "IF Attendance is Critically Low AND Makeup is Partial THEN Debarment Risk is High AND Ineligible for Final Exam (Sec 1.27.1)."),
        FuzzyRule("R_ATT_03", [("Attendance_Pct", "Critically_Low"), ("Remedial_Makeup_Score", "Fully_Certified")],
                  [("Debarment_Risk", "Caution_Borderline"), ("Exam_Eligibility", "Conditional_Tutorial")],
                  "IF Attendance is Critically Low BUT Makeup is Fully Certified THEN Debarment Risk is Caution AND Exam is Conditional Tutorial (Sec 1.27.2)."),
        FuzzyRule("R_ATT_04", [("Attendance_Pct", "Shortfall_Borderline"), ("Remedial_Makeup_Score", "None_Unapproved")],
                  [("Debarment_Risk", "High_Risk"), ("Exam_Eligibility", "Ineligible_Barred")],
                  "IF Attendance is Shortfall Borderline (<75%) AND Makeup is None THEN High Risk AND Ineligible for Final Exam (Sec 1.27.1)."),
        FuzzyRule("R_ATT_05", [("Attendance_Pct", "Shortfall_Borderline"), ("Remedial_Makeup_Score", "Partial_Makeup")],
                  [("Debarment_Risk", "Caution_Borderline"), ("Exam_Eligibility", "Conditional_Tutorial")],
                  "IF Attendance is Shortfall Borderline AND Makeup is Partial THEN Caution Borderline AND Conditional Tutorial (Sec 1.27.2)."),
        FuzzyRule("R_ATT_06", [("Attendance_Pct", "Shortfall_Borderline"), ("Remedial_Makeup_Score", "Fully_Certified")],
                  [("Debarment_Risk", "Safe"), ("Exam_Eligibility", "Fully_Eligible")],
                  "IF Attendance is Shortfall Borderline AND Makeup is Fully Certified THEN Safe AND Fully Eligible (Sec 1.27.2)."),
        FuzzyRule("R_ATT_07", [("Attendance_Pct", "Safe_Adequate")],
                  [("Debarment_Risk", "Safe"), ("Exam_Eligibility", "Fully_Eligible")],
                  "IF Attendance is Safe/Adequate (>=75%) THEN Debarment Risk is Safe AND Fully Eligible (Sec 1.27.1)."),
        FuzzyRule("R_ATT_08", [("Attendance_Pct", "Exemplary")],
                  [("Debarment_Risk", "Safe"), ("Exam_Eligibility", "Fully_Eligible")],
                  "IF Attendance is Exemplary THEN Debarment Risk is Safe AND Fully Eligible (Sec 1.27.1).")
    ]

    return FuzzySubsystem("Class Attendance & Exam Eligibility (Section 1.27)",
                          {"Attendance_Pct": att_pct, "Remedial_Makeup_Score": remedial_score},
                          {"Debarment_Risk": debarment_risk, "Exam_Eligibility": exam_eligibility},
                          rules)

# ==============================================================================
# 2. Course Withdrawal & Fee Adjustment Subsystem (Section 1.14.2 - 1.14.4)
# ==============================================================================
def build_withdrawal_subsystem() -> FuzzySubsystem:
    withdrawal_day = LinguisticVariable(
        name="Withdrawal_Day",
        unit="Days (Semester Timeline)",
        universe=(0.0, 70.0),
        terms={
            "Week_1_Initial": Trapmf(0.0, 0.0, 6.0, 7.8),
            "Week_2_AddDrop": Trimf(6.5, 11.0, 15.8),
            "Weeks_3_to_7_Regular": Trapmf(14.5, 20.0, 48.0, 50.5),
            "Post_Week_7_Late": Trapmf(48.5, 52.0, 70.0, 70.0)
        }
    )

    transcript_penalty = LinguisticVariable(
        name="Transcript_Penalty_Severity",
        unit="index 0-100",
        universe=(0.0, 100.0),
        terms={
            "Clean_No_Record": Trapmf(0.0, 0.0, 15.0, 25.0),
            "Recorded_W_Grade": Trimf(20.0, 50.0, 75.0),
            "Disallowed_Withdrawal": Trapmf(70.0, 85.0, 100.0, 100.0)
        }
    )

    fee_refund = LinguisticVariable(
        name="Fee_Refund_Adjustment_Pct",
        unit="%",
        universe=(0.0, 100.0),
        terms={
            "No_Adjustment": Trapmf(0.0, 0.0, 10.0, 25.0),
            "Half_Adjustment_50Pct": Trimf(20.0, 50.0, 75.0),
            "Full_Adjustment_100Pct": Trapmf(70.0, 85.0, 100.0, 100.0)
        }
    )

    rules = [
        FuzzyRule("R_WDL_01", [("Withdrawal_Day", "Week_1_Initial")],
                  [("Transcript_Penalty_Severity", "Clean_No_Record"), ("Fee_Refund_Adjustment_Pct", "Full_Adjustment_100Pct")],
                  "IF Withdrawal is in Week 1 (Days <=7) THEN Clean Record (No record on transcript) AND Full Fee Adjustment (Sec 1.14.2, 1.14.4)."),
        FuzzyRule("R_WDL_02", [("Withdrawal_Day", "Week_2_AddDrop")],
                  [("Transcript_Penalty_Severity", "Clean_No_Record"), ("Fee_Refund_Adjustment_Pct", "Half_Adjustment_50Pct")],
                  "IF Withdrawal is in Week 2 (Days <=15) THEN Clean Record (No record) AND Half Fee Adjustment (Sec 1.14.2, 1.14.4)."),
        FuzzyRule("R_WDL_03", [("Withdrawal_Day", "Weeks_3_to_7_Regular")],
                  [("Transcript_Penalty_Severity", "Recorded_W_Grade"), ("Fee_Refund_Adjustment_Pct", "No_Adjustment")],
                  "IF Withdrawal is between Week 3 and Week 7 (Days 16-49) THEN Transcript receives 'W' Grade AND No Fee Adjustment (Sec 1.14.3, 1.14.4)."),
        FuzzyRule("R_WDL_04", [("Withdrawal_Day", "Post_Week_7_Late")],
                  [("Transcript_Penalty_Severity", "Disallowed_Withdrawal"), ("Fee_Refund_Adjustment_Pct", "No_Adjustment")],
                  "IF Withdrawal is after Week 7 (Day >49) THEN Withdrawal Disallowed (Remains Enrolled / Default F) AND No Fee Adjustment (Sec 1.14.3, 1.14.4).")
    ]

    return FuzzySubsystem("Course Withdrawal & Fee Adjustment (Section 1.14)",
                          {"Withdrawal_Day": withdrawal_day},
                          {"Transcript_Penalty_Severity": transcript_penalty, "Fee_Refund_Adjustment_Pct": fee_refund},
                          rules)

# ==============================================================================
# 3. Repeating a Course Subsystem (Section 1.17.1 - 1.17.2)
# ==============================================================================
def build_repeat_subsystem() -> FuzzySubsystem:
    course_grade = LinguisticVariable(
        name="Earned_Course_GPA",
        unit="Grade Point (0.0-4.0)",
        universe=(0.0, 4.0),
        terms={
            "Failing_Low": Trapmf(0.0, 0.0, 1.0, 1.7),
            "Repeat_Eligible_C": Trimf(1.4, 2.0, 2.52),
            "Borderline_C_Plus": Trimf(2.45, 2.52, 2.65),
            "Above_C_Plus_Ineligible": Trapmf(2.55, 2.85, 4.0, 4.0)
        }
    )

    class_size = LinguisticVariable(
        name="Cohort_Enrolled_Size",
        unit="Students Enrolled",
        universe=(0.0, 30.0),
        terms={
            "Deficit_Under_10": Trapmf(0.0, 0.0, 6.0, 9.5),
            "Quorum_Met": Trimf(8.8, 12.0, 18.0),
            "Full_Class": Trapmf(15.0, 20.0, 30.0, 30.0)
        }
    )

    repeat_permission = LinguisticVariable(
        name="Repeat_Permission_Index",
        unit="index 0-100",
        universe=(0.0, 100.0),
        terms={
            "Denied_Ineligible": Trapmf(0.0, 0.0, 15.0, 30.0),
            "Conditional_Quorum_Pending": Trimf(25.0, 50.0, 70.0),
            "Approved_Permitted": Trapmf(65.0, 85.0, 100.0, 100.0)
        }
    )

    cgpa_impact = LinguisticVariable(
        name="CGPA_Improvement_Impact",
        unit="index 0-100",
        universe=(0.0, 100.0),
        terms={
            "Minimal_Gain": Trapmf(0.0, 0.0, 20.0, 35.0),
            "Moderate_Gain": Trimf(30.0, 55.0, 75.0),
            "Maximum_Recovery": Trapmf(70.0, 85.0, 100.0, 100.0)
        }
    )

    rules = [
        FuzzyRule("R_REP_01", [("Earned_Course_GPA", "Failing_Low"), ("Cohort_Enrolled_Size", "Full_Class")],
                  [("Repeat_Permission_Index", "Approved_Permitted"), ("CGPA_Improvement_Impact", "Maximum_Recovery")],
                  "IF Grade is Failing/Low AND Class Size is Full THEN Repeat Approved AND Maximum Recovery Potential (Sec 1.17.1, 1.17.2)."),
        FuzzyRule("R_REP_02", [("Earned_Course_GPA", "Failing_Low"), ("Cohort_Enrolled_Size", "Quorum_Met")],
                  [("Repeat_Permission_Index", "Approved_Permitted"), ("CGPA_Improvement_Impact", "Maximum_Recovery")],
                  "IF Grade is Failing/Low AND Quorum Met (>=10) THEN Repeat Approved AND Maximum Recovery Potential (Sec 1.17.1, 1.17.2)."),
        FuzzyRule("R_REP_03", [("Earned_Course_GPA", "Failing_Low"), ("Cohort_Enrolled_Size", "Deficit_Under_10")],
                  [("Repeat_Permission_Index", "Conditional_Quorum_Pending"), ("CGPA_Improvement_Impact", "Maximum_Recovery")],
                  "IF Grade is Failing/Low BUT Class Size < 10 THEN Permission Conditional on Quorum Meeting 10 students (Sec 1.17.2)."),
        FuzzyRule("R_REP_04", [("Earned_Course_GPA", "Repeat_Eligible_C"), ("Cohort_Enrolled_Size", "Full_Class")],
                  [("Repeat_Permission_Index", "Approved_Permitted"), ("CGPA_Improvement_Impact", "Moderate_Gain")],
                  "IF Grade is C or C+ (<=2.5) AND Class Full THEN Repeat Approved AND Moderate Recovery Gain (Sec 1.17.1)."),
        FuzzyRule("R_REP_05", [("Earned_Course_GPA", "Repeat_Eligible_C"), ("Cohort_Enrolled_Size", "Quorum_Met")],
                  [("Repeat_Permission_Index", "Approved_Permitted"), ("CGPA_Improvement_Impact", "Moderate_Gain")],
                  "IF Grade is C or C+ (<=2.5) AND Quorum Met THEN Repeat Approved AND Moderate Recovery Gain (Sec 1.17.1, 1.17.2)."),
        FuzzyRule("R_REP_06", [("Earned_Course_GPA", "Repeat_Eligible_C"), ("Cohort_Enrolled_Size", "Deficit_Under_10")],
                  [("Repeat_Permission_Index", "Conditional_Quorum_Pending"), ("CGPA_Improvement_Impact", "Moderate_Gain")],
                  "IF Grade is C/C+ BUT Class Size < 10 THEN Repeat Conditional on reaching minimum 10 students (Sec 1.17.2)."),
        FuzzyRule("R_REP_07", [("Earned_Course_GPA", "Borderline_C_Plus"), ("Cohort_Enrolled_Size", "Quorum_Met")],
                  [("Repeat_Permission_Index", "Conditional_Quorum_Pending"), ("CGPA_Improvement_Impact", "Moderate_Gain")],
                  "IF Grade is Borderline C+ (~2.5) AND Quorum Met THEN Repeat Conditional on HoD Verification (Sec 1.17.1, 1.17.2)."),
        FuzzyRule("R_REP_08", [("Earned_Course_GPA", "Above_C_Plus_Ineligible")],
                  [("Repeat_Permission_Index", "Denied_Ineligible"), ("CGPA_Improvement_Impact", "Minimal_Gain")],
                  "IF Grade is Above C+ (>2.5 GP) THEN Repeat Denied (Ineligible to repeat grade > 2.5) (Sec 1.17.1).")
    ]

    return FuzzySubsystem("Repeating a Course (Section 1.17)",
                          {"Earned_Course_GPA": course_grade, "Cohort_Enrolled_Size": class_size},
                          {"Repeat_Permission_Index": repeat_permission, "CGPA_Improvement_Impact": cgpa_impact},
                          rules)

# ==============================================================================
# 4. Probation and Drop Rules Subsystem (Section 5.5.1 - 5.5.5)
# ==============================================================================
def build_probation_subsystem() -> FuzzySubsystem:
    cgpa_margin = LinguisticVariable(
        name="CGPA_Margin",
        unit="Delta to Program Min (-2.0 to +2.0)",
        universe=(-2.0, 2.0),
        terms={
            "Severe_Deficit": Trapmf(-2.0, -2.0, -0.6, -0.2),
            "Marginal_Deficit": Trimf(-0.35, -0.1, 0.02),
            "Satisfactory_Clear": Trimf(-0.01, 0.3, 0.7),
            "Good_High_Standing": Trapmf(0.5, 0.9, 2.0, 2.0)
        }
    )

    consecutive_prob = LinguisticVariable(
        name="Consecutive_Probations",
        unit="Count (0 to 3)",
        universe=(0.0, 3.0),
        terms={
            "Zero_Probation": Trapmf(0.0, 0.0, 0.2, 0.7),
            "One_Probation": Trimf(0.5, 1.0, 1.5),
            "Two_Probations": Trapmf(1.4, 2.0, 3.0, 3.0)
        }
    )

    academic_risk = LinguisticVariable(
        name="Academic_Risk_Severity",
        unit="index 0-100",
        universe=(0.0, 100.0),
        terms={
            "Good_Standing": Trapmf(0.0, 0.0, 15.0, 30.0),
            "Advisory_Warning": Trimf(20.0, 40.0, 60.0),
            "Probation_Alert": Trimf(50.0, 70.0, 85.0),
            "Severe_Drop_Threat": Trapmf(75.0, 90.0, 100.0, 100.0)
        }
    )

    registration_action = LinguisticVariable(
        name="Registration_Action_Advisory",
        unit="index 0-100",
        universe=(0.0, 100.0),
        terms={
            "Registration_Barred_Drop": Trapmf(0.0, 0.0, 15.0, 30.0),
            "Principal_Approval_Mandatory": Trimf(25.0, 45.0, 65.0),
            "Academic_Counseling_Required": Trimf(50.0, 70.0, 85.0),
            "Unrestricted_Registration": Trapmf(75.0, 90.0, 100.0, 100.0)
        }
    )

    rules = [
        FuzzyRule("R_PRB_01", [("CGPA_Margin", "Good_High_Standing")],
                  [("Academic_Risk_Severity", "Good_Standing"), ("Registration_Action_Advisory", "Unrestricted_Registration")],
                  "IF CGPA Margin is High Standing THEN Academic Risk is Good Standing AND Unrestricted Registration (Sec 5.5.1)."),
        FuzzyRule("R_PRB_02", [("CGPA_Margin", "Satisfactory_Clear"), ("Consecutive_Probations", "Zero_Probation")],
                  [("Academic_Risk_Severity", "Good_Standing"), ("Registration_Action_Advisory", "Unrestricted_Registration")],
                  "IF CGPA Margin is Satisfactory Clear AND Zero Probations THEN Good Standing AND Unrestricted Registration (Sec 5.5.1)."),
        FuzzyRule("R_PRB_03", [("CGPA_Margin", "Satisfactory_Clear"), ("Consecutive_Probations", "One_Probation")],
                  [("Academic_Risk_Severity", "Good_Standing"), ("Registration_Action_Advisory", "Unrestricted_Registration")],
                  "IF CGPA >= Minimum after 1 Probation THEN Count Resets to Zero AND Good Standing (Sec 5.5.4 Reset Rule)."),
        FuzzyRule("R_PRB_04", [("CGPA_Margin", "Satisfactory_Clear"), ("Consecutive_Probations", "Two_Probations")],
                  [("Academic_Risk_Severity", "Advisory_Warning"), ("Registration_Action_Advisory", "Unrestricted_Registration")],
                  "IF CGPA >= Minimum after 2 Probations THEN Probation Reset with Advisory Warning AND Unrestricted Registration (Sec 5.5.4)."),
        FuzzyRule("R_PRB_05", [("CGPA_Margin", "Marginal_Deficit"), ("Consecutive_Probations", "Zero_Probation")],
                  [("Academic_Risk_Severity", "Advisory_Warning"), ("Registration_Action_Advisory", "Academic_Counseling_Required")],
                  "IF CGPA is Marginal Deficit (< Min) on 0 Probations THEN Placed on 1st Probation / Advisory Warning AND Counseling Required (Sec 5.5.1, 5.5.2)."),
        FuzzyRule("R_PRB_06", [("CGPA_Margin", "Marginal_Deficit"), ("Consecutive_Probations", "One_Probation")],
                  [("Academic_Risk_Severity", "Probation_Alert"), ("Registration_Action_Advisory", "Academic_Counseling_Required")],
                  "IF CGPA is Marginal Deficit on 1st Probation THEN 2nd Consecutive Probation Alert (Formal Warning Issued) (Sec 5.5.1, 5.5.2)."),
        FuzzyRule("R_PRB_07", [("CGPA_Margin", "Marginal_Deficit"), ("Consecutive_Probations", "Two_Probations")],
                  [("Academic_Risk_Severity", "Severe_Drop_Threat"), ("Registration_Action_Advisory", "Principal_Approval_Mandatory")],
                  "IF CGPA is Marginal Deficit on 2nd Probation THEN Severe Drop Threat AND Registration Requires Prior Principal Approval (Sec 5.5.3, 5.5.5)."),
        FuzzyRule("R_PRB_08", [("CGPA_Margin", "Severe_Deficit"), ("Consecutive_Probations", "Zero_Probation")],
                  [("Academic_Risk_Severity", "Probation_Alert"), ("Registration_Action_Advisory", "Academic_Counseling_Required")],
                  "IF CGPA is Severe Deficit on 0 Probations THEN 1st Probation Alert AND Academic Counseling Mandated (Sec 5.5.1)."),
        FuzzyRule("R_PRB_09", [("CGPA_Margin", "Severe_Deficit"), ("Consecutive_Probations", "One_Probation")],
                  [("Academic_Risk_Severity", "Severe_Drop_Threat"), ("Registration_Action_Advisory", "Principal_Approval_Mandatory")],
                  "IF CGPA is Severe Deficit on 1st Probation THEN High Drop Threat AND Principal Approval Mandatory (Sec 5.5.2, 5.5.5)."),
        FuzzyRule("R_PRB_10", [("CGPA_Margin", "Severe_Deficit"), ("Consecutive_Probations", "Two_Probations")],
                  [("Academic_Risk_Severity", "Severe_Drop_Threat"), ("Registration_Action_Advisory", "Registration_Barred_Drop")],
                  "IF CGPA is Deficit after 2 Consecutive Probations THEN Immediate Drop from Academic Programme AND Barred from Registration (Sec 5.5.3).")
    ]

    return FuzzySubsystem("Probation and Drop Rules (Section 5.5)",
                          {"CGPA_Margin": cgpa_margin, "Consecutive_Probations": consecutive_prob},
                          {"Academic_Risk_Severity": academic_risk, "Registration_Action_Advisory": registration_action},
                          rules)

PROGRAM_MIN_CGPA = {
    "BS / BBA / BEE": 2.00,
    "Associate Degree (AD)": 2.00,
    "MS / MPhil / MBA": 2.50,
    "PhD": 3.00
}
