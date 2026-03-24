import numpy as np
import os
import cv2
import svgwrite
from PIL import Image
import matplotlib.pyplot as plt
import random
import base64  
import re
from image_similarity_measures.evaluate import evaluation

from bs4 import BeautifulSoup

decomposed_images=[]

existing_regions = []
aspectRatio_existing = []

element_count_dict = {}  


probabilidade = 0.9  
quality_ratio = 0.1

def decidir_guardar_imagem(probabilidade):
    return random.random() < probabilidade

def save_transparent_png(image, path):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(image)
    rgba = [b, g, r, alpha]
    transparent_image = cv2.merge(rgba, 4)
    cv2.imwrite(path, transparent_image)

def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

def calculate_similarity(image1, image2, metric="ssim"):
    similarity_dict = evaluation(org_img_path=image1, pred_img_path=image2, metrics=[metric])
    similarity_value = similarity_dict[metric]
    return similarity_value

def add_region_if_unique(aspectRatio_existing, aspectRatio, element_path_temp, existing_regions, similarity_threshold=0.75):
    image1 = str(element_path_temp)
    aspectRatio_tolerance = 0.1

    for i, existing_region in enumerate(existing_regions):
        aspectRatio2 = aspectRatio_existing[i]
        image2 = str(existing_region)

        if abs(aspectRatio - aspectRatio2) < aspectRatio_tolerance:
            similarity_value = calculate_similarity(image1, image2, metric="ssim")
            if similarity_value > similarity_threshold:
                return False

    existing_regions.append(element_path_temp)
    aspectRatio_existing.append(aspectRatio)
    return True


def decompose(array_images, searchTerm, semanticWords, galleryType='sebastiao'):
    saved_png_files = [] 
    saved_png_files_name = []
    decomposed_info = []
    self_path = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(self_path, ".."))
    elements_folder = os.path.join(self_path, "static", "elements")
    temp_elements_folder = os.path.join(self_path, "static", "temp_elements")
    png_elements_folder = os.path.join(self_path, "static", "elements_png")
    os.makedirs(elements_folder, exist_ok=True)
    os.makedirs(temp_elements_folder, exist_ok=True)
    os.makedirs(png_elements_folder, exist_ok=True)
    counter = 0 
    contador = 0
    counter_temp = 0
    existing_elements = [file for file in os.listdir(elements_folder) if file.endswith(".svg")]
    for existing_element in existing_elements:
        element_path = os.path.join(elements_folder, existing_element)
        os.remove(element_path)

    existing_elements = [file for file in os.listdir(png_elements_folder) if file.endswith(".png")]
    for existing_element in existing_elements:
        element_path = os.path.join(png_elements_folder, existing_element)
        os.remove(element_path)

    for item in array_images:

        existing_regions.clear()
        aspectRatio_existing.clear()
        existing_elements = [file for file in os.listdir(temp_elements_folder) if file.endswith(".tiff")]
        for existing_element in existing_elements:
            element_path = os.path.join(temp_elements_folder, existing_element)
            os.remove(element_path)
        counter_limit = 0
        contador += 1
        if galleryType == 'my':
            img_path = os.path.normpath(
                os.path.join(project_root, "frontend", "public", "static", "UserUploads", str(item['id_imagem']))
            )
        else:
            img_path = os.path.normpath(
                os.path.join(project_root, "frontend", "public", "static", "InputWorks", str(item['id_imagem']))
            )

        image = cv2.imread(img_path)
        if image is None:
            continue
        img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        vectorized = img.reshape((-1,3))
        vectorized = np.float32(vectorized)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 9
        attempts = 5
        ret,label,center=cv2.kmeans(vectorized,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        result_image = res.reshape((img.shape))
        result_image_hsv = cv2.cvtColor(result_image, cv2.COLOR_RGB2HSV)
        b, g, r = cv2.split(result_image_hsv)
        result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
        image_gray=cv2.cvtColor(result_image_rgb, cv2.COLOR_BGR2GRAY)
        _, image_threshold = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        _, image_threshold_1 = cv2.threshold(image_gray, 85, 255, cv2.THRESH_BINARY_INV)
        lower_yellow = np.array([150, 150, 0])
        upper_yellow = np.array([255, 255, 100])
        lower_cyan = np.array([0, 100, 100])
        upper_cyan = np.array([100, 255, 255])
        lower_magenta = np.array([100, 0, 100])
        upper_magenta = np.array([255, 100, 255])
        mser = cv2.MSER_create()
        regions, _ = mser.detectRegions(image_threshold)
        regions_1, _ = mser.detectRegions(image_threshold_1)
        regions_b, _ = mser.detectRegions(b)
        regions_g, _ = mser.detectRegions(g)
        regions_r, _ = mser.detectRegions(r)

        yellow_mask = cv2.inRange(result_image, lower_yellow, upper_yellow)
        cyan_mask = cv2.inRange(result_image, lower_cyan, upper_cyan)
        magenta_mask = cv2.inRange(result_image, lower_magenta, upper_magenta)

        contours_yellow, _ = mser.detectRegions(yellow_mask)
        contours_cyan, _ = mser.detectRegions(cyan_mask)
        contours_magenta, _ = mser.detectRegions(magenta_mask)

        all_contours = []
        all_contours.extend(regions)
        all_contours.extend(regions_1)
        all_contours.extend(regions_b)
        all_contours.extend(regions_g)
        all_contours.extend(regions_r)
        all_contours.extend(contours_yellow)
        all_contours.extend(contours_cyan)
        all_contours.extend(contours_magenta)    

        for i, region in enumerate(all_contours):
            area = cv2.contourArea(region)
            x, y, w, h = cv2.boundingRect(region)
            bounding_box_area = w * h
            region_quality = area / bounding_box_area
            min_area = 90  
            max_area = 5000
            min_region_quality = 0 
            max_region_quality = 1  
            normalized_region_quality = normalize(region_quality, min_region_quality, max_region_quality)
            original_height, original_width, _ = image.shape
            original_bounding_box_area = original_width * original_height
            if counter_limit<=30:
                if area > min_area and area < max_area and area < original_bounding_box_area/2 and w > original_width/80 and h > original_height/80: 
                    if normalized_region_quality > quality_ratio:
                        mask = np.zeros_like(image, dtype=np.uint8)
                        cv2.drawContours(mask, [region], 0, (255, 255, 255), thickness=cv2.FILLED)
                        masked_image = cv2.bitwise_and(image, mask)
                        x, y, w, h = cv2.boundingRect(region)
                        element = masked_image[y:y+h, x:x+w]

                        image_gray = cv2.cvtColor(element, cv2.COLOR_BGR2GRAY)
                        _, alpha = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY)
                        b, g, r = cv2.split(element)
                        rgba = [b, g, r, alpha]
                        transparent_image = cv2.merge(rgba, 4)

                        _, buffer = cv2.imencode('.png', cv2.cvtColor(transparent_image, cv2.COLOR_BGR2BGRA))
                        encoded_image = base64.b64encode(buffer)

                        element_svg_path = os.path.join(elements_folder, f"{item['id_imagem']}_{i+1}.svg")
                        element_path_temp = os.path.join(temp_elements_folder, f"{counter_temp}.tiff")
                        element_png_path = os.path.join(png_elements_folder, f"{counter_temp}.png")

                        
                        target_size = (800, 600)
                        resized_element = cv2.resize(transparent_image, target_size, interpolation=cv2.INTER_AREA)

                        cv2.imwrite(element_path_temp, resized_element)
                        
                        aspectRatio = w / h

                        if len(existing_regions) == 0:
                            dwg = svgwrite.Drawing(element_svg_path, profile='tiny', size=(f"{w}px", f"{h}px"))
                            dwg.add(dwg.image(href=f"data:image/png;base64,{encoded_image.decode('utf-8')}", size=(f"{w}px", f"{h}px"), opacity=1.0))
                            dwg.save()
                            cv2.imwrite(element_png_path, transparent_image)
                            saved_png_files.append(f"frontend/public/static/elements_png/{counter_temp}.png")
                            saved_png_files_name.append(f"frontend/public/static/elements_png_name/{counter_temp}_{item['id_imagem']}.png")                       
                            existing_regions.append(element_path_temp)                       
                            counter_temp += 1
                            aspectRatio_existing.append(aspectRatio)
                            counter += 1
                            counter_limit += 1
                             
                        elif add_region_if_unique(aspectRatio_existing, aspectRatio, element_path_temp, existing_regions, similarity_threshold=0.75):
                            dwg = svgwrite.Drawing(element_svg_path, profile='tiny', size=(f"{w}px", f"{h}px"))
                            dwg.add(dwg.image(href=f"data:image/png;base64,{encoded_image.decode('utf-8')}", size=(f"{w}px", f"{h}px"), opacity=1.0))
                            dwg.save()
                            cv2.imwrite(element_png_path, transparent_image)
                            saved_png_files.append(f"/static/elements_png/{counter_temp}.png")
                            saved_png_files_name.append(f"/static/elements_png_name/{counter_temp}_{item['id_imagem']}.png")
                            counter += 1
                            counter_limit += 1
                            counter_temp += 1
                        
                    elif decidir_guardar_imagem(probabilidade):
                        mask = np.zeros_like(image, dtype=np.uint8)
                        cv2.drawContours(mask, [region], 0, (255, 255, 255), thickness=cv2.FILLED)
                        masked_image = cv2.bitwise_and(image, mask)
                        x, y, w, h = cv2.boundingRect(region)
                        element = masked_image[y:y+h, x:x+w]
                        image_gray = cv2.cvtColor(element, cv2.COLOR_BGR2GRAY)
                        _, alpha = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY)
                        b, g, r = cv2.split(element)
                        rgba = [b, g, r, alpha]
                        transparent_image = cv2.merge(rgba, 4)
                        _, buffer = cv2.imencode('.png', cv2.cvtColor(transparent_image, cv2.COLOR_BGR2BGRA))
                        encoded_image = base64.b64encode(buffer)
                        element_svg_path = os.path.join(elements_folder, f"{item['id_imagem']}_{i+1}.svg")
                        element_path_temp = os.path.join(temp_elements_folder, f"{counter_temp}.tiff")
                        element_png_path = os.path.join(png_elements_folder, f"{counter_temp}.png")
                        target_size = (800, 600)
                        resized_element = cv2.resize(transparent_image, target_size, interpolation=cv2.INTER_AREA)
                        cv2.imwrite(element_path_temp, resized_element)                        
                        aspectRatio = w / h
                        if len(existing_regions) == 0:
                            dwg = svgwrite.Drawing(element_svg_path, profile='tiny', size=(f"{w}px", f"{h}px"))
                            dwg.add(dwg.image(href=f"data:image/png;base64,{encoded_image.decode('utf-8')}", size=(f"{w}px", f"{h}px"), opacity=1.0))
                            dwg.save()                        
                            cv2.imwrite(element_png_path, transparent_image)
                            saved_png_files.append(f"/static/elements_png/{counter_temp}.png")
                            saved_png_files_name.append(f"/static/elements_png_name/{counter_temp}_{item['id_imagem']}.png")                   
                            existing_regions.append(element_path_temp)
                            counter_temp += 1
                            aspectRatio_existing.append(aspectRatio)
                            counter += 1
                            counter_limit += 1
                             
                        elif add_region_if_unique(aspectRatio_existing, aspectRatio, element_path_temp, existing_regions, similarity_threshold=0.85):
                            dwg = svgwrite.Drawing(element_svg_path, profile='tiny', size=(f"{w}px", f"{h}px"))
                            dwg.add(dwg.image(href=f"data:image/png;base64,{encoded_image.decode('utf-8')}", size=(f"{w}px", f"{h}px"), opacity=1.0))
                            dwg.save()
                            cv2.imwrite(element_png_path, transparent_image)
                            saved_png_files.append(f"/static/elements_png/{counter_temp}.png")
                            saved_png_files_name.append(f"/static/elements_png_name/{counter_temp}_{item['id_imagem']}.png")
                            counter += 1
                            counter_limit += 1
                            counter_temp += 1
    
        palavras_chave = item.get("palavras_chave", []) if isinstance(item, dict) else []
        prob = item.get("prob", []) if isinstance(item, dict) else []
        seen = set()
        unique_palavras_chave = []
        unique_prob = []
        for idx, palavra in enumerate(palavras_chave):
            if palavra not in seen:
                seen.add(palavra)
                unique_palavras_chave.append(palavra)
                if idx < len(prob):
                    unique_prob.append(prob[idx])

        info = {
            "id_imagem": item["id_imagem"] if isinstance(item, dict) and "id_imagem" in item else str(item),
            "palavras_chave": unique_palavras_chave,
            "prob": unique_prob,
            "relation": item.get("relation", "") if isinstance(item, dict) else ""
        }
        decomposed_info.append(info)
    return saved_png_files, saved_png_files_name, decomposed_info