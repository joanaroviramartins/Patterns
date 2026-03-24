import random
import os
from PIL import Image
import math

solutions_history = []
images = []
imagesChosen = []
solution_info = []
image_indices = []
composition_area = 600 * 600
scale = concentration = space = rhythm = transparency = value = 0
total_element_width = 0
principles = []

def load_images(folder_path):
    images_general = []
    image_extensions = (".jpg", ".jpeg", ".png", ".tif", ".svg")
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path).convert("RGBA")
            images_general.append(image)
    return images_general

def setting_up_solutions ():
    self_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    elements_folder = os.path.join(self_path, "frontend/public/static/elements_png")
    images = load_images(elements_folder)
    elements_n = random.randint(2, 7)
    
    image_indices = random.sample(range(len(images)), elements_n)
    value = random.randint(0, 100)
    transparency = random.randint(0, 100)
    motion = random.randint(0, 100)
    scale = random.randint(0, 100)
    space = random.randint(0, 100)
    concentration = random.randint(0, 100)

    solution_info = {
        "elements number": elements_n,
        "src": image_indices ,  # Imagens da library
        "principles": {
            "value": value,
            "transparency": transparency,
            "motion": motion,
            "scale": scale,
            "space": space,
            "concentration": concentration,
        },
    }
    solutions_history.append(solution_info)
    return solution_info  

