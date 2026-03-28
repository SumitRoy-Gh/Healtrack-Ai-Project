import cv2
import numpy as np
from PIL import Image
import torch
from torchvision import transforms

def load_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not found or corrupted. Check the path: " + image_path)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img_rgb

def resize_image(img_rgb):
    resized = cv2.resize(img_rgb, (224, 224))
    return resized

def extract_redness(img_rgb):
    red_channel = img_rgb[:, :, 0]
    redness = red_channel.mean() / 255.0
    return float(redness)

def to_tensor(img_rgb):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    pil_img = Image.fromarray(img_rgb)
    tensor = transform(pil_img)
    tensor = tensor.unsqueeze(0)

    return tensor

def detect_wound_region(img_rgb):
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

    lower = np.array([0, 40, 40])
    upper = np.array([20, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return {"mask": mask, "area": 0.0, "contour": None}

    largest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest)

    return {
        "mask": mask,
        "area": float(area),
        "contour": largest
    }

def preprocess(image_path):
    img_rgb = load_image(image_path)

    resized_rgb = resize_image(img_rgb)

    redness = extract_redness(resized_rgb)

    wound_data = detect_wound_region(resized_rgb)

    tensor = to_tensor(resized_rgb)

    result = {
        "tensor": tensor,
        "img_rgb": resized_rgb,
        "redness": redness,
        "mask": wound_data["mask"],
        "wound_area": wound_data["area"]
    }

    return result

if __name__ == "__main__":
    print("Testing preprocessing pipeline...")

    result = preprocess("data/patient_001/day1.jpg")
    

    print("Redness score:", result["redness"])
    print("Image shape:", result["img_rgb"].shape)
    print("Tensor shape:", result["tensor"].shape)
    print("Wound area (pixels):", result["wound_area"])
    print("Mask shape:", result["mask"].shape)
    print("All good! Preprocessing working correctly.")

