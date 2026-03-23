import os
from PIL import Image

input_folder = "input_images"
output_folder = "augmented_images"

os.makedirs(output_folder, exist_ok=True)

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

for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".png", ".jpeg")):
        path = os.path.join(input_folder, filename)
        img = Image.open(path).convert("RGB")

        name = os.path.splitext(filename)[0]

        img.save(os.path.join(output_folder, f"{name}_original.jpg"))

        zoom_levels = [1.1, 1.2, 1.3, 1.4]

        for i, z in enumerate(zoom_levels):
            zoomed = zoom_image(img, z)
            zoomed.save(os.path.join(output_folder, f"{name}_zoom{i+1}.jpg"))

print("Done! Images saved in augmented_images/")
