import numpy as np

def normalise_size_change(area_today, area_yesterday):
    if area_yesterday == 0:
        return 0.0

    change = (area_today - area_yesterday) / area_yesterday
    change = np.clip(change, -1, 1)

    normalised = (change + 1) / 2

    return float(normalised)

def compute_healing_score(redness, size_change_norm, change_score):
    score = (
        0.40 * (1 - redness) +
        0.40 * (1 - size_change_norm) +
        0.20 * (1 - change_score)
    ) * 100

    score = np.clip(score, 0, 100)
    score = round(float(score), 1)

    return score

def get_status(score_today, score_yesterday):
    if score_yesterday is None:
        return "Baseline"

    diff = score_today - score_yesterday

    if diff > 1:
        return f"Improving ↑ (+{round(diff, 1)})"

    if diff < -1:
        return f"Worsening ↓ ({round(diff, 1)})"

    return "Stable →"

def compute(redness, area_today, area_yesterday, change_score, prev_score):
    size_change_norm = normalise_size_change(area_today, area_yesterday)

    score = compute_healing_score(redness, size_change_norm, change_score)

    status = get_status(score, prev_score)

    return {
        "healing_score": score,
        "status": status
    }

if __name__ == "__main__":
    print("Testing Healing Score...")

    redness = 0.4
    area_today = 800
    area_yesterday = 1000
    change_score = 0.1
    prev_score = 65

    result = compute(redness, area_today, area_yesterday, change_score, prev_score)

    print("Healing Score:", result["healing_score"])
    print("Status:", result["status"])
