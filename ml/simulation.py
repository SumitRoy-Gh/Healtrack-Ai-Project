import cv2
import numpy as np
from PIL import Image, ImageDraw
import os


def compute_deltas(history):
    if len(history) < 2:
        return {"redness_delta": 0.0, "area_delta": 0.0}

    redness_delta = history[-1]["redness"] - history[-2]["redness"]

    prev_area = max(history[-2]["area"], 1)
    area_delta = (history[-1]["area"] - history[-2]["area"]) / prev_area

    return {
        "redness_delta": redness_delta,
        "area_delta":    area_delta
    }


def simulate_future(img_rgb, mask, redness_delta, area_delta):
    predicted = img_rgb.copy()

    coords = np.where(mask > 0)

    if len(coords[0]) > 0:
        wound_px = predicted[coords]

        mult = 1 + min(redness_delta * 1.3, 0.3)
        wound_px[:, 0] = np.clip(wound_px[:, 0] * mult, 0, 255)

        predicted[coords] = wound_px

    kernel = np.ones((7, 7), np.uint8)

    if area_delta > 0.05:
        expanded_mask = cv2.dilate(mask, kernel, iterations=1)
    elif area_delta < -0.05:
        expanded_mask = cv2.erode(mask, kernel, iterations=1)
    else:
        expanded_mask = mask

    coords_expanded = np.where(expanded_mask > 0)
    predicted[coords_expanded] = predicted[coords_expanded]

    pil_img = Image.fromarray(predicted)
    draw    = ImageDraw.Draw(pil_img)
    draw.text((10, 10), "PREDICTED — Day+2", fill=(255, 0, 0))

    predicted = np.array(pil_img)

    return predicted


def save_predicted_image(img_rgb, path):
    bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, bgr)


def run_simulation(image_path, history, patient_id, day):
    """
    Master function — combines all simulation steps.
    This is what pipeline.py imports and calls.

    Input  : image_path (string) — path to today's wound image
             history    (list)   — list of daily records
             patient_id (string) — e.g. "patient_001"
             day        (int)    — current day number
    Output : dict with predicted image array and saved path
    """
    from preprocessing import preprocess

    # Step 1: Load and preprocess the image
    print("  [Simulation] Loading image...")
    result  = preprocess(image_path)
    img_rgb = result["img_rgb"]
    mask    = result["mask"]

    # Step 2: Calculate how much redness and area changed recently
    print("  [Simulation] Computing trend deltas...")
    deltas        = compute_deltas(history)
    redness_delta = deltas["redness_delta"]
    area_delta    = deltas["area_delta"]

    print(f"  [Simulation] Redness delta : {redness_delta:.3f}")
    print(f"  [Simulation] Area delta    : {area_delta:.3f}")

    # Step 3: Generate the predicted future image
    print("  [Simulation] Generating predicted image...")
    predicted_img = simulate_future(img_rgb, mask, redness_delta, area_delta)

    # Step 4: Save the predicted image to disk
    os.makedirs("outputs/predicted", exist_ok=True)
    save_path = f"outputs/predicted/{patient_id}_day{day}_predicted.jpg"

    save_predicted_image(predicted_img, save_path)
    print(f"  [Simulation] Saved: {save_path}")

    return {
        "predicted_image":      predicted_img,
        "predicted_image_path": save_path
    }


if __name__ == "__main__":
    print("Testing Simulation...")

    img  = cv2.imread("data/patient_001/day1.jpg")
    img  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    mask = np.zeros((224, 224), dtype=np.uint8)
    mask[80:150, 80:150] = 255

    predicted = simulate_future(img, mask, 0.1, 0.2)

    save_predicted_image(predicted, "outputs_predicted.jpg")

    print("Saved predicted image as outputs_predicted.jpg")