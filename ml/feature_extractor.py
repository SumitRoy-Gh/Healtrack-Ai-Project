import torch
import torchvision.models as models
import numpy as np

def load_model():
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

    model = torch.nn.Sequential(*list(model.children())[:-1])

    model.eval()

    return model

def extract_features(tensor, model):
    with torch.no_grad():
        features = model(tensor)

    vec = features.squeeze().numpy()

    assert vec.shape == (512,), f"Expected (512,), got {vec.shape}"

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm

    return vec

def save_vector(vec, path):
    np.save(path, vec)

def load_vector(path):
    vec = np.load(path)
    return vec

if __name__ == "__main__":
    print("Testing feature extractor...")

    from preprocessing import preprocess

    model = load_model()

    result = preprocess("data/patient_001/day1.jpg")

    tensor = result["tensor"]

    vec = extract_features(tensor, model)

    print("Feature vector shape:", vec.shape)
    print("First 5 values:", vec[:5])
    print("Norm:", np.linalg.norm(vec))

    print("All good! Feature extraction working.")

    