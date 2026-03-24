import os
from PIL import Image
from flask import jsonify

def get_images_data():
    self_path = os.path.abspath(os.path.dirname(__file__))
    elements_folder = os.path.join(self_path, "../frontend/public/static/InputWorks")
    if not os.path.exists(elements_folder):
        raise FileNotFoundError(f"Error: Directory '{elements_folder}' does not exist.")

    images_data = []
    for filename in os.listdir(elements_folder):
        if filename.lower().endswith(".jpg"):
            jpg_path = os.path.join(elements_folder, filename)
            with Image.open(jpg_path) as img:
                width, height = img.size
            if width > height:
                orientation = "horizontal"
            elif height > width:
                orientation = "vertical"
            else:
                orientation = "square"

            images_data.append({
                "filename": filename,
                "path": f"static/InputWorks/{filename}",
                "orientation": orientation,
                "width": width,
                "height": height,
            })

    for image in images_data:
        print(f"Image path found: {image['path']}")
    return images_data
