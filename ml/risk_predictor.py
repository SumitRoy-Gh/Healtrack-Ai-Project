# No imports needed — pure Python logic

def compute_risk(redness_trend, area_trend, change_score, score_drop):
    risk = 0
    contributing_factors = []

    if redness_trend == "rising":
        risk += 40
        contributing_factors.append("Redness increasing over multiple days")

    if area_trend == "growing":
        risk += 30
        contributing_factors.append("Wound area growing")

    if change_score > 0.4:
        risk += 25
        contributing_factors.append("Large texture change detected")

    if score_drop > 10:
        risk += 20
        contributing_factors.append("Significant score drop from previous day")

    risk = min(risk, 95)

    if risk < 25:
        level = "Low"
    elif risk < 50:
        level = "Medium"
    elif risk < 75:
        level = "High"
    else:
        level = "Critical"

    return {
        "risk_pct": risk,
        "risk_level": level,
        "contributing_factors": contributing_factors
    }


if __name__ == "__main__":
    print("Testing Risk Predictor...")

    result = compute_risk(
        redness_trend="rising",
        area_trend="growing",
        change_score=0.5,
        score_drop=12
    )

    print("Risk %:", result["risk_pct"])
    print("Risk Level:", result["risk_level"])
    print("Factors:", result["contributing_factors"])