from PIL import Image, ImageDraw, ImageOps
import io
import base64
import math
import requests
import random
import colorsys
import os

def generating(imgData, imagesInfo, output_filepath):
    try:
        canvas_image = Image.open(io.BytesIO(base64.b64decode(imgData.split(",")[1])))
        canvas_width, canvas_height = canvas_image.size

        margin = 100
        new_width = canvas_width + 2 * margin
        new_height = canvas_height + 2 * margin

        canvas = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 0))

        for info in imagesInfo:
            image_url = info["image"]
            x = int(info["x"])
            y = int(info["y"])
            width = int(info["width"])
            height = int(info["height"])
            rotation_radians = info["rotation"]
            opacity = info["opacity"]

            rotation_degrees = -math.degrees(rotation_radians)

            if "elements_png" in image_url:
                local_path = image_url.split("/static/")[-1]
                local_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "frontend", "public", "static", local_path)
                if os.path.exists(local_path):
                    image = Image.open(local_path).convert("RGBA")
                else:
                    image = Image.open(io.BytesIO(requests.get(image_url).content)).convert("RGBA")
            else:
                image = Image.open(io.BytesIO(requests.get(image_url).content)).convert("RGBA")
            image = image.convert("RGBA")
            image = image.resize((width, height), Image.Resampling.LANCZOS)

            effective_opacity = max(opacity, 0.2)  

            r, g, b, a = image.split() 
            new_alpha = Image.eval(a, lambda p: int(p * effective_opacity))  
            transparent_image = Image.merge("RGBA", (r, g, b, new_alpha))
            rotated_image = transparent_image.rotate(rotation_degrees, expand=True)
            rotated_width, rotated_height = rotated_image.size
            center_x = margin + x + width // 2
            center_y = margin + y + height // 2

            paste_position = (
                center_x - rotated_width // 2,
                center_y - rotated_height // 2,
            )

            canvas.paste(rotated_image, paste_position, rotated_image)

        canvas.save(output_filepath)
        expand(imagesInfo, output_filepath, canvas_width)
    except Exception as e:
        print(f"Error generating the image: {e}")

def expand (imagesInfo, output_filepath, canvas_width): 
    repetitions = 4
    margin = 100
    imagesChosen = []
    structure_type = random.random()
    structure_type_thresholds = [
        (0, 0.06), (0.06, 0.12), (0.12, 0.19), (0.19, 0.25), (0.25, 0.31),
        (0.31, 0.37), (0.37, 0.43), (0.43, 0.50), (0.50, 0.56), (0.56, 0.62),
        (0.62, 0.68), (0.68, 0.74), (0.74, 0.80), (0.80, 0.84), (0.84, 0.87),
        (0.87, 1)
    ]
    for i, (low, high) in enumerate(structure_type_thresholds):
        if low < structure_type <= high:
            print(f"structureType: {i + 1} ({structure_type})")
            break

    image = Image.open(output_filepath)    
    img_width, img_height = image.size
    
    real_width = img_width - margin * 2
    real_height = img_height - margin * 2
    
    canvas_width = real_width * repetitions
    canvas_height = real_height * repetitions

    background_color = imagesInfo[0]["backgroundColor"]
    
    if background_color == "#FFFFFF":
        rgba_color = (255, 255, 255, 255)  
    elif background_color == "#000000":
        rgba_color = (0, 0, 0, 255)  
    else:
        rgba_color = hsl_to_rgba(background_color, alpha=255)

    canvas = Image.new("RGBA", (canvas_width, canvas_height), rgba_color) 
    canvas.paste(Image.new("RGBA", (canvas_width, canvas_height), rgba_color), (0, 0))
    
    for i in range(repetitions):
        for j in range(repetitions):
            x_offset = i * real_width - margin   
            y_offset = j * real_height - margin  

            image_info = {
                "image": image,  
                "index": (i, j),  
                "size": (real_width, real_height),
                "position": (x_offset, y_offset) 
            }
            imagesChosen.append(image_info)
    

    gene_x = 0
    gene_y = 0
    gene = (gene_x, gene_y)
    pos_x = gene_x - margin
    pos_y = gene_y - margin

    for i, img_info in enumerate(imagesChosen):
        pos_x, pos_y = img_info["position"]
        img = img_info["image"]
        img_width, img_height = img_info["size"]
        img_translate = img_height / 4
        if structure_type < 0.06:
            if i % 4 == 1:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif i % 4 == 2:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            elif i % 4 == 3:
                img = img.transpose(Image.ROTATE_180)
        elif 0.06 < structure_type <= 0.12:
            if i % 4 == 1 or i % 4 == 3:
                img = img.transpose(Image.ROTATE_180)
        elif 0.12 < structure_type <= 0.19:
            if i % 4 == 2 or i % 4 == 3:
                img = img.transpose(Image.ROTATE_180)
        elif 0.19 < structure_type <= 0.25:
            if i % 4 == 0 or i % 4 == 2:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            if i % 4 == 1 or i % 4 == 3:
                img = img.transpose(Image.ROTATE_180)
        elif 0.25 < structure_type <= 0.31:
            if i % 4 == 1 or i % 4 == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif 0.31 < structure_type <= 0.37:
            if i % 4 == 0 or i % 4 == 3:
                img = img.transpose(Image.ROTATE_180)
            if i % 4 == 1 or i % 4 == 2:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
        elif 0.37 < structure_type <= 0.43:
            if i % 4 == 0:
                gene = (gene[0], gene[1] + img_translate)
            elif i % 4 == 1:
                gene = (gene[0], gene[1] - img_translate)
            elif i % 4 == 2:
                gene = (gene[0], gene[1] + img_translate)
            elif i % 4 == 3:
                gene = (gene[0], gene[1] - img_translate)
        elif 0.43 < structure_type <= 0.50:
            angle = 30
            if i % 4 == 1:
                img = img.rotate(angle)
            elif i % 4 == 2:
                img = img.rotate(-angle)
            elif i % 4 == 3:
                img = img.rotate(angle)
        elif 0.50 < structure_type <= 0.56:
            angle = 45
            if i % 4 == 0:
                img = img.rotate(angle)
                gene = (gene[0], gene[1] + img_translate)
            elif i % 4 == 1:
                img = img.rotate(-angle)
                gene = (gene[0], gene[1] - img_translate)
            elif i % 4 == 2:
                img = img.rotate(angle)
                gene = (gene[0], gene[1] + img_translate)
            elif i % 4 == 3:
                img = img.rotate(angle)
                gene = (gene[0], gene[1] - img_translate)
        elif 0.56 < structure_type <= 0.62:
            angle = 90
            if i % 4 == 0 or i % 4 == 2:
                img = img.rotate(angle)
            elif i % 4 == 1 or i % 4 == 3:
                img = img.rotate(-angle)
        elif 0.62 < structure_type <= 0.68:
            angle = 180
            if i % 4 == 1 or i % 4 == 3:
                img = img.rotate(angle)
        elif 0.68 < structure_type <= 0.74:
            angle = 90
            if i % 4 == 1 or i % 4 == 3:
                img = img.rotate(-angle)
            elif 0.74 < structure_type <= 0.80:
                angle = 45
                if i % 4 == 0 or i % 4 == 2:
                    img = img.rotate(angle)
                    gene = (gene[0] + img_translate, gene[1])
        elif 0.80 < structure_type <= 0.84:
            angle = 90
            if i % 4 == 0 or i % 4 == 2:
                img = img.rotate(angle)
                gene = (gene[0], gene[1] + img_translate)
        elif 0.84 < structure_type <= 0.87:
            angle = -45
            if i % 4 == 1 or i % 4 == 3:
                img = img.rotate(angle)
                gene = (gene[0], gene[1] - img_translate)
        elif 0.87 < structure_type <= 1:
            angle = 45
            if i % 4 == 0 or i % 4 == 2:
                img = img.rotate(angle)
                gene = (gene[0] + img_translate, gene[1])
        canvas.paste(img, (int(pos_x), int(pos_y)), img)
    canvas.save(output_filepath)

def hsl_to_rgba(hsl, alpha=255):
    hsl = hsl.strip('hsl()').split(',')  
    h, s, l = [float(x.strip('%')) / 100 if '%' in x else float(x) for x in hsl]
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return (r, g, b, alpha)