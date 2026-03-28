import requests
import json


# -----------------------------------------
# 1. Build Prompt from Payload
# -----------------------------------------
def build_prompt(payload):
    return f"""
You are a clinical monitoring assistant for wound care.
Analyse the following wound monitoring data and return a JSON response.

Patient ID: {payload['patient_id']}
Monitoring Day: {payload['day']}
Healing Score: {payload['healing_score']}/100
Status: {payload['status']}
Trend: {payload['trend']}
Redness Level: {payload['redness']}
Wound Area: {payload['wound_area']} pixels
Infection Risk: {payload['infection_risk_pct']}% ({payload['risk_level']})
Flagged Factors: {', '.join(payload['contributing_factors']) if payload['contributing_factors'] else 'None'}

Return ONLY valid JSON.
No explanation. No extra text.

Format:
{{
  "doctor_summary": "3-4 sentence clinical summary ending with: This is a monitoring signal only — clinical judgment required.",
  "patient_advice": ["Advice 1", "Advice 2", "Advice 3"]
}}
"""


# -----------------------------------------
# 2. Call Ollama Local Model
# -----------------------------------------
def generate_report_local(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "mistral",   # you can change to llama3 if installed
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        result = response.json()
        return result.get("response", "")
    except Exception as e:
        print("Error calling Ollama:", e)
        return ""


# -----------------------------------------
# 3. Safe JSON Parsing
# -----------------------------------------
def safe_parse(text):
    try:
        return json.loads(text)
    except:
        print("⚠️ JSON parsing failed. Using fallback report.")

        return {
            "doctor_summary": "Report generation failed. Please review raw data manually. This is a monitoring signal only — clinical judgment required.",
            "patient_advice": [
                "Monitor wound daily.",
                "Keep wound clean and dry.",
                "Consult a doctor if symptoms worsen."
            ]
        }


# -----------------------------------------
# 4. Main Function (used in pipeline)
# -----------------------------------------
def generate_report(payload):
    prompt = build_prompt(payload)

    raw_text = generate_report_local(prompt)

    result = safe_parse(raw_text)

    return result


# -----------------------------------------
# 5. Optional: Cache Report (Save to file)
# -----------------------------------------
def cache_report(patient_id, day, report):
    import os

    folder = f"data/{patient_id}"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/day{day}_report.json"

    with open(path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"Report saved at {path}")


# -----------------------------------------
# 6. Test Block
# -----------------------------------------
if __name__ == "__main__":
    print("Testing Report Generator (Ollama)...")

    sample_payload = {
        "patient_id": "P001",
        "day": 3,
        "healing_score": 72.5,
        "status": "Improving ↑",
        "trend": "Improving",
        "redness": 0.45,
        "wound_area": 1200,
        "infection_risk_pct": 35,
        "risk_level": "Medium",
        "contributing_factors": ["Wound area growing"]
    }

    report = generate_report(sample_payload)

    print("\nGenerated Report:")
    print(report)

    cache_report("P001", 3, report)
