import json
import os
import numpy as np


def load_history(patient_id):
    path = f"data/{patient_id}/history.json"

    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        history = json.load(f)

    return history


def save_day_record(patient_id, record):
    path = f"data/{patient_id}/history.json"

    history = load_history(patient_id)

    history.append(record)

    with open(path, "w") as f:
        json.dump(history, f, indent=4)


def compute_trend(history):
    if len(history) < 2:
        return "Insufficient Data"

    recent = history[-3:]
    scores = [r["healing_score"] for r in recent]

    slope = scores[-1] - scores[0]

    if slope > 3:
        return "Improving"

    if slope < -3:
        return "Declining"

    if max(scores) - min(scores) <= 2:
        return "Stalled"

    return "Stable"


def compute_redness_trend(history):
    if len(history) < 2:
        return "insufficient"

    recent = history[-3:]
    values = [r["redness"] for r in recent]

    if all(x < y for x, y in zip(values, values[1:])):
        return "rising"

    if all(x > y for x, y in zip(values, values[1:])):
        return "falling"

    return "stable"


def compute_area_trend(history):
    if len(history) < 2:
        return "insufficient"

    recent = history[-3:]
    values = [r["area"] for r in recent]

    if all(x < y for x, y in zip(values, values[1:])):
        return "growing"

    if all(x > y for x, y in zip(values, values[1:])):
        return "shrinking"

    return "stable"


if __name__ == "__main__":
    print("Testing Trend Analysis...")

    test_history = [
        {"day": 1, "redness": 0.5, "area": 1200, "healing_score": 60},
        {"day": 2, "redness": 0.4, "area": 1000, "healing_score": 66},
        {"day": 3, "redness": 0.35, "area": 800, "healing_score": 72},
    ]

    print("Trend:", compute_trend(test_history))
    print("Redness Trend:", compute_redness_trend(test_history))
    print("Area Trend:", compute_area_trend(test_history))

    