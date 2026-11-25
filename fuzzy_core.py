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
Bahria University Academic Regulations - Fuzzy Inference System (FIS) Core Engine
Implements Mamdani Fuzzy Inference with Centroid Defuzzification
"""

import numpy as np
from typing import Dict, List, Tuple, Any

class MembershipFunction:
    def __call__(self, x: float) -> float:
        raise NotImplementedError

class Trimf(MembershipFunction):
    """Triangular Membership Function defined by [a, b, c]"""
    def __init__(self, a: float, b: float, c: float):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)

    def __call__(self, x: float) -> float:
        if x <= self.a or x >= self.c:
            return 0.0
        elif self.a < x <= self.b:
            if self.b == self.a:
                return 1.0
            return (x - self.a) / (self.b - self.a)
        elif self.b < x < self.c:
            if self.c == self.b:
                return 1.0
            return (self.c - x) / (self.c - self.b)
        return 0.0

class Trapmf(MembershipFunction):
    """Trapezoidal Membership Function defined by [a, b, c, d]"""
    def __init__(self, a: float, b: float, c: float, d: float):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)

    def __call__(self, x: float) -> float:
        if x < self.a or x > self.d:
            return 0.0
        elif self.a <= x <= self.b:
            if self.b == self.a:
                return 1.0
            return (x - self.a) / (self.b - self.a)
        elif self.b < x <= self.c:
            return 1.0
        elif self.c < x <= self.d:
            if self.d == self.c:
                return 1.0
            return (self.d - x) / (self.d - self.c)
        return 0.0

class LinguisticVariable:
    """Represents a linguistic input or output variable with a universe of discourse."""
    def __init__(self, name: str, unit: str, universe: Tuple[float, float], terms: Dict[str, MembershipFunction]):
        self.name = name
        self.unit = unit
        self.universe = universe
        self.terms = terms

    def evaluate_terms(self, x: float) -> Dict[str, float]:
        return {term: mf(x) for term, mf in self.terms.items()}

class FuzzyRule:
    """
    Represents an IF-THEN fuzzy rule.
    antecedent: List of tuples (var_name, term_name) combined via fuzzy AND (min)
    consequent: List of tuples (var_name, term_name)
    rule_id: identifier (e.g. 'R_ATT_01')
    description: natural language description
    """
    def __init__(self, rule_id: str, antecedent: List[Tuple[str, str]], consequent: List[Tuple[str, str]], description: str = ""):
        self.rule_id = rule_id
        self.antecedent = antecedent
        self.consequent = consequent
        self.description = description

class FuzzySubsystem:
    """Mamdani Fuzzy Subsystem for a specific domain module."""
    def __init__(self, name: str, inputs: Dict[str, LinguisticVariable], outputs: Dict[str, LinguisticVariable], rules: List[FuzzyRule]):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.rules = rules

    def infer(self, input_values: Dict[str, float], num_samples: int = 500) -> Dict[str, Any]:
        """
        Executes Mamdani Min-Max inference and Centroid Defuzzification.
        Returns:
            crisp_outputs: Dict[var_name, float]
            linguistic_labels: Dict[var_name, str]
            fired_rules: List[Dict containing rule_id, strength, desc]
            output_distributions: Dict[var_name, (x_vals, y_vals)]
        """
        # Step 1: Fuzzification
        fuzzified: Dict[str, Dict[str, float]] = {}
        for var_name, var in self.inputs.items():
            val = input_values.get(var_name, var.universe[0])
            # Bound within universe
            val_clamped = max(var.universe[0], min(var.universe[1], val))
            fuzzified[var_name] = var.evaluate_terms(val_clamped)

        # Step 2: Rule Evaluation (Mamdani Min implication)
        fired_rules = []
        # Store for each output variable, the aggregated fuzzy set
        aggregated_sets: Dict[str, Tuple[np.ndarray, np.ndarray]] = {}
        for out_name, out_var in self.outputs.items():
            x_vals = np.linspace(out_var.universe[0], out_var.universe[1], num_samples)
            y_vals = np.zeros(num_samples)
            aggregated_sets[out_name] = (x_vals, y_vals)

        for rule in self.rules:
            # Evaluate antecedent using MIN
            strengths = []
            for var_name, term_name in rule.antecedent:
                deg = fuzzified[var_name].get(term_name, 0.0)
                strengths.append(deg)
            firing_strength = min(strengths) if strengths else 0.0

            if firing_strength > 0.001:
                fired_rules.append({
                    "rule_id": rule.rule_id,
                    "strength": round(firing_strength, 4),
                    "description": rule.description,
                    "consequent": rule.consequent
                })

                # Implication & Aggregation (MAX across rules)
                for out_name, term_name in rule.consequent:
                    x_vals, y_vals = aggregated_sets[out_name]
                    mf = self.outputs[out_name].terms[term_name]
                    # Compute clipped fuzzy output: min(firing_strength, mf(x))
                    term_y = np.array([min(firing_strength, mf(x)) for x in x_vals])
                    aggregated_sets[out_name] = (x_vals, np.maximum(y_vals, term_y))

        # Step 3: Defuzzification (Centroid method)
        crisp_outputs = {}
        linguistic_labels = {}
        for out_name, (x_vals, y_vals) in aggregated_sets.items():
            out_var = self.outputs[out_name]
            total_area = np.sum(y_vals)
            if total_area > 1e-9:
                crisp_val = np.sum(x_vals * y_vals) / total_area
            else:
                # Fallback to midpoint of universe if no rule fired
                crisp_val = (out_var.universe[0] + out_var.universe[1]) / 2.0
            
            crisp_outputs[out_name] = round(float(crisp_val), 2)
            
            # Determine dominant linguistic term
            term_memberships = out_var.evaluate_terms(crisp_val)
            dominant_term = max(term_memberships.items(), key=lambda item: item[1])[0]
            linguistic_labels[out_name] = dominant_term

        # Sort fired rules by strength descending
        fired_rules.sort(key=lambda r: r["strength"], reverse=True)

        return {
            "crisp_outputs": crisp_outputs,
            "linguistic_labels": linguistic_labels,
            "fired_rules": fired_rules,
            "aggregated_sets": aggregated_sets,
            "fuzzified_inputs": fuzzified
        }
