import os
import random
from PIL import Image, ImageEnhance, ImageFilter
import zipfile

input_root = "input_images"
output_root = "dataset"

classes = os.listdir(input_root)

# Create folders
for split in ["train", "test"]:
    for cls in classes:
        os.makedirs(f"{output_root}/{split}/{cls}", exist_ok=True)

# Zoom function
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

# Augmentation
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

# Process all images
for cls in classes:
    class_path = os.path.join(input_root, cls)
    images = [f for f in os.listdir(class_path) if f.endswith((".jpg", ".png", ".jpeg"))]

    counter = 0

    for img_name in images:
        path = os.path.join(class_path, img_name)
        original = Image.open(path).convert("RGB")

        # Create multiple versions per image
        for i in range(5):  # 5 augmentations per image
            img = original.copy()
            if i != 0:
                img = augment(img)

            split = "train" if random.random() < 0.8 else "test"
            save_path = f"{output_root}/{split}/{cls}/{cls}_{counter}.jpg"
            img.save(save_path)
            counter += 1

# Zip dataset
with zipfile.ZipFile("dataset.zip", "w") as z:
    for root, _, files in os.walk(output_root):
        for f in files:
            full = os.path.join(root, f)
            z.write(full, os.path.relpath(full, output_root))

print("DONE: dataset.zip created with multiple images + zoom")
