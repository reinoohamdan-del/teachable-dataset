import os
import random
from PIL import Image, ImageEnhance, ImageFilter
import zipfile

# Classes and input images
images = {
    "Ethan": "input_images/ethan.jpg",
    "Suspect": "input_images/suspect.jpg",
    "Ramirez": "input_images/ramirez.jpg"
}

# Create folders
for split in ["train", "test"]:
    for cls in images:
        os.makedirs(f"dataset/{split}/{cls}", exist_ok=True)

# ✅ Zoom function
def zoom_image(img, zoom_factor):
    w, h = img.size
    new_w = int(w / zoom_factor)
    new_h = int(h / zoom_factor)

    left = (w - new_w) // 2
    top = (h - new_h) // 2
    right = left + new_w
    bottom = top + new_h

    cropped = img.crop((left, top, right, bottom))
    return cropped.resize((w, h))

# Augmentation function
def augment(img):
    choice = random.choice(["rotate", "bright", "contrast", "blur", "zoom"])
    
    if choice == "rotate":
        return img.rotate(random.uniform(-10, 10))
    elif choice == "bright":
        return ImageEnhance.Brightness(img).enhance(random.uniform(0.8,1.2))
    elif choice == "contrast":
        return ImageEnhance.Contrast(img).enhance(random.uniform(0.8,1.2))
    elif choice == "blur":
        return img.filter(ImageFilter.GaussianBlur(1))
    elif choice == "zoom":
        return zoom_image(img, random.uniform(1.1, 1.4))
    
    return img

# Generate dataset
for cls, path in images.items():
    original = Image.open(path).convert("RGB")

    for i in range(20):
        img = original.copy()

        # Keep first image original
        if i != 0:
            img = augment(img)

        folder = "train" if i < 16 else "test"
        img.save(f"dataset/{folder}/{cls}/{cls.lower()}_{i}.jpg")

# Zip dataset
with zipfile.ZipFile("dataset.zip", "w") as z:
    for root, _, files in os.walk("dataset"):
        for f in files:
            full = os.path.join(root, f)
            z.write(full, os.path.relpath(full, "dataset"))

print("DONE: dataset.zip created with zoom augmentation")
