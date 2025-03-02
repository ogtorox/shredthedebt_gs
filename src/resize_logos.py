import os
from PIL import Image

TARGET_HEIGHT = 80  # Bars are usually not tall, so make these small
TARGET_ASPECT_RATIO = 1  # e.g., 3:1 (3x wider than tall)

# Paths
input_folder = "../logos"    # Where your original images are
output_folder = "../shredthedebt_gs"  # Where resized images will be saved

os.makedirs(output_folder, exist_ok=True)

def resize_image(input_path, output_path):
    img = Image.open(input_path)

    target_width = int(TARGET_HEIGHT * TARGET_ASPECT_RATIO)
    img = img.resize((target_width, TARGET_HEIGHT), Image.Resampling.LANCZOS)

    img.save(output_path)
    print(f"Resized {input_path} -> {output_path}")

def batch_resize():
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            resize_image(input_path, output_path)

if __name__ == "__main__":
    batch_resize()
    print("All logos resized and saved.")