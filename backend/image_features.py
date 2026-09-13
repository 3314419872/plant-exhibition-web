import io

import numpy as np
from PIL import Image


def load_image_from_bytes(data: bytes):
    return Image.open(io.BytesIO(data)).convert("RGB")


def load_image_from_path(path: str):
    return Image.open(path).convert("RGB")


def extract_features(image):
    image = image.convert("RGB").resize((256, 256))
    arr = np.asarray(image, dtype=np.float32) / 255.0

    r_hist = np.histogram(arr[:, :, 0], bins=8, range=(0.0, 1.0))[0]
    g_hist = np.histogram(arr[:, :, 1], bins=8, range=(0.0, 1.0))[0]
    b_hist = np.histogram(arr[:, :, 2], bins=8, range=(0.0, 1.0))[0]

    feature = np.concatenate([r_hist, g_hist, b_hist]).astype(np.float32)
    norm = np.linalg.norm(feature)
    if norm > 0:
        feature = feature / norm
    return feature


def cosine_similarity(vec_a, vec_b):
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
