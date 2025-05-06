import os
from PIL import Image

TARGET_SIZE = (200, 200)  # width x height in pixels
INPUT_FOLDER = "../resized_logos"  # original images
OUTPUT_FOLDER = "../shredthedebt_gs/head_pngs"  # resized PNGs

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def resize_image(input_path, output_path):
    with Image.open(input_path) as img:
        img = img.convert("RGBA")  # ensures transparency support
        resized = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        resized.save(output_path, format="PNG")
        print(f"✅ Resized: {os.path.basename(input_path)} -> {output_path}")

def batch_resize():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_filename = os.path.splitext(filename)[0] + ".png"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            resize_image(input_path, output_path)

if __name__ == "__main__":
    batch_resize()
    print("🎉 All logos resized to 200x200px and saved as PNG.")