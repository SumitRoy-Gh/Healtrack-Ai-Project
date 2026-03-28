import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import cv2

def compute_similarity(vec_today, vec_yesterday):
    if vec_yesterday is None:
        return {
            "similarity": 1.0,
            "change_score": 0.0
        }

    vec_today_2d = vec_today.reshape(1, -1)
    vec_yesterday_2d = vec_yesterday.reshape(1, -1)

    sim = cosine_similarity(vec_today_2d, vec_yesterday_2d)[0][0]

    # Clamp similarity to valid range
    sim = float(np.clip(sim, -1.0, 1.0))

    change_score = 1 - sim

    # Ensure change_score is non-negative
    change_score = float(max(0.0, change_score))
    

    return {
        "similarity": float(sim),
        "change_score": float(change_score)
    }

def pixel_diff(img_today, img_yesterday):
    if img_yesterday is None:
        return 0.0

    diff = cv2.absdiff(img_today, img_yesterday)

    mean_diff = diff.mean()

    return float(mean_diff)


if __name__ == "__main__":
    print("Testing similarity module...")

    from preprocessing import preprocess
    from feature_extractor import load_model, extract_features

    model = load_model()

    # Day 1 image
    result1 = preprocess("data/patient_001/day1.jpg")
    tensor1 = result1["tensor"]
    img1 = result1["img_rgb"]

    vec1 = extract_features(tensor1, model)

    # Simulate Day 2 (use same image for now)
    result2 = preprocess("data/patient_001/day1.jpg")
    tensor2 = result2["tensor"]
    img2 = result2["img_rgb"]

    vec2 = extract_features(tensor2, model)

    sim_result = compute_similarity(vec1, vec2)

    pixel_change = pixel_diff(img1, img2)

    print("Similarity:", sim_result["similarity"])
    print("Change Score:", sim_result["change_score"])
    print("Pixel Difference:", pixel_change)

    print("All good! Similarity working.")