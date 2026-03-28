def build_payload(patient_id, day, preprocessing_result, score_result, risk_result, trend_label):
        payload = {
        "patient_id": patient_id,
        "day": day,
        "healing_score": score_result["healing_score"],
        "status": score_result["status"],
        "trend": trend_label,
        "redness": round(preprocessing_result["redness"], 3),
        "wound_area": preprocessing_result["wound_area"],
        "infection_risk_pct": risk_result["risk_pct"],
        "risk_level": risk_result["risk_level"],
        "contributing_factors": risk_result["contributing_factors"]
    }
        return payload


def validate_payload(payload):
        required_keys = [
        "patient_id",
        "day",
        "healing_score",
        "status",
        "trend",
        "redness",
        "wound_area",
        "infection_risk_pct",
        "risk_level",
        "contributing_factors"
    ]
        for key in required_keys:
            if key not in payload:
                raise ValueError(f"Missing field: {key}")
            if payload[key] is None:
                raise ValueError(f"Field is None: {key}")
            
if __name__ == "__main__":

    import json
    from report_generator import generate_report
    from simulation import run_simulation
    from visualisation import export_all_charts
    import cv2

    print("=" * 55)
    print("  HealTrack AI — Full Pipeline Test")
    print("=" * 55)

    # ── Step 1: Define test inputs ─────────────────────────
    patient_id = "patient_001"
    day        = 3
    image_path = "data/patient_001/day1.jpg"

    # ── Step 2: Build the payload (your existing logic) ────
    print("\n[1/5] Building analytics payload...")

    payload = {
        "patient_id":          patient_id,
        "day":                 day,
        "healing_score":       72.5,
        "status":              "Improving ↑",
        "trend":               "Improving",
        "redness":             0.45,
        "wound_area":          1200,
        "infection_risk_pct":  35,
        "risk_level":          "Medium",
        "contributing_factors": ["Wound area growing"]
    }

    print("  Payload ready:")
    print(" ", payload)

    # ── Step 3: Generate the doctor report using Ollama ────
    print("\n[2/5] Generating doctor report via Ollama Mistral...")
    print("  (This may take 10-20 seconds — Ollama is thinking...)")

    report = generate_report(payload)

    print("\n  ── DOCTOR SUMMARY ──────────────────────────")
    print(" ", report["doctor_summary"])

    print("\n  ── PATIENT ADVICE ──────────────────────────")
    for i, advice in enumerate(report["patient_advice"], 1):
        print(f"  {i}. {advice}")

    # ── Step 4: Generate predicted future image ────────────
    print("\n[3/5] Generating predicted future wound image...")

    # Fake history for simulation delta calculation
    fake_history = [
        {"day": 1, "redness": 0.60, "area": 1500, "healing_score": 55},
        {"day": 2, "redness": 0.52, "area": 1350, "healing_score": 63},
        {"day": 3, "redness": 0.45, "area": 1200, "healing_score": 72},
    ]

    import os
    os.makedirs("outputs/predicted", exist_ok=True)

    simulation_result = run_simulation(
        image_path = image_path,
        history    = fake_history,
        patient_id = patient_id,
        day        = day
    )

    predicted_path = simulation_result["predicted_image_path"]
    print("  Predicted image saved at:", predicted_path)
    print("  Open that file to see the simulated future wound.")

    # ── Step 5: Generate and save all charts ───────────────
    print("\n[4/5] Generating charts...")

    chart_jsons = export_all_charts(
        history    = fake_history,
        risk_pct   = payload["infection_risk_pct"],
        patient_id = patient_id,
        day        = day
    )

    print("  Charts saved in outputs/charts/")

    # ── Step 6: Print final summary ────────────────────────
    print("\n[5/5] Final Summary")
    print("=" * 55)
    print(f"  Patient       : {payload['patient_id']}")
    print(f"  Day           : {payload['day']}")
    print(f"  Healing Score : {payload['healing_score']} / 100")
    print(f"  Status        : {payload['status']}")
    print(f"  Trend         : {payload['trend']}")
    print(f"  Infection Risk: {payload['infection_risk_pct']}% ({payload['risk_level']})")
    print(f"  Predicted Image: {predicted_path}")
    print(f"  Charts        : outputs/charts/")
    print("=" * 55)
    print("\n  ML Pipeline fully complete!")