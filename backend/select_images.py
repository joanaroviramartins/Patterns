from nltk.corpus import wordnet
import json
from PIL import Image
import io
import os
from transformers import CLIPProcessor, CLIPModel
from bs4 import BeautifulSoup
import requests


related_images = []


hiponimos=[]
hiperonimos=[]
sinonimos=[]

inputWord_semAspas = None

warning_message = ""

def get_relation(word_list, word2, word_relations):
    word2_with_underscore = word2.replace(" ", "_")
    for word_relation in word_relations:
        word = word_relation['palavra']
        sinonimos = word_relation['sinonimos']
        hiperonimos = word_relation['hiperonimos']
        hiponimos = word_relation['hiponimos']
        if word2_with_underscore in sinonimos:
            return f"{word} and {word2} are synonyms"

        if word2_with_underscore in hiperonimos:
            return f"{word} is a hypernym of {word2}"

        if word2_with_underscore in hiponimos:
            return f"{word} is a hyponym of {word2}"
    return f"The words in the list and {word2} do not have a clear relation in the provided arrays."


def get_related_words(input_words):
    related_words = []
    related_words = set(input_words)
    words_info = []

    for word in input_words:
        word_info = {'palavra': word, 'sinonimos': [], 'hiperonimos': [], 'hiponimos': []}
        synonyms = wordnet.synsets(word)
        for synset in synonyms:
            related_words.update([lemma.name() for lemma in synset.lemmas()])
            word_info['sinonimos'].extend([lemma.name() for lemma in synset.lemmas()])

            for hypernym in synset.hypernyms():
                related_words.update([lemma.name() for lemma in hypernym.lemmas()])
                word_info['hiperonimos'].extend([lemma.name() for lemma in hypernym.lemmas()])

            for hyponym in synset.hyponyms():
                related_words.update([lemma.name() for lemma in hyponym.lemmas()])
                word_info['hiponimos'].extend([lemma.name() for lemma in hyponym.lemmas()])

        words_info.append(word_info)
    return related_words, words_info

def process_images(folder_path, relatedWords, rate=0.70):
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=True)
    image_extensions = (".jpg", ".jpeg", ".png", ".tif")
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            with Image.open(image_path) as img:
                width, height = img.size
                if width > height:
                    orientation = "horizontal"
                elif height > width:
                    orientation = "vertical"
                else:
                    orientation = "square"
            inputs = processor(text=relatedWords, images=image, return_tensors="pt", padding=True)
            outputs = model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)
            resultado_imagem = {"id_imagem": filename, 
                                "palavras_chave": [], 
                                "prob": [], 
                                "orientation": orientation,  
                                "width": width,
                                "height": height,}

            for i, tensor_val in enumerate(probs[0]):
                try:
                    value = float(tensor_val.item())
                except Exception:
                    try:
                        value = float(tensor_val)
                    except Exception:
                        continue

                if value > float(rate):
                    keyword = relatedWords[i]
                    resultado_imagem["palavras_chave"].append(keyword)
                    resultado_imagem["prob"].append(value)
                    existente_index = next((index for (index, item) in enumerate(related_images) if item.get("id_imagem") == resultado_imagem["id_imagem"]), None)

                    if existente_index is not None:
                        existing_probs = related_images[existente_index].get("prob", [])
                        try:
                            existing_first = float(existing_probs[0]) if existing_probs else -1.0
                        except Exception:
                            existing_first = -1.0

                        if resultado_imagem["prob"][0] > existing_first:
                            related_images[existente_index] = resultado_imagem
                    else:
                        related_images.append(resultado_imagem)


def find_related_images(input_words, userSelectedImages):
    if related_images:
        related_images.clear()

    input_words = [word.strip() for word in input_words.strip('"').split(',')]

    related_words, words_info = get_related_words(input_words)
    relatedWords = [s.replace('_', ' ') for s in related_words]

    for imagem in userSelectedImages:
        if isinstance(imagem, dict):
            filename = imagem.get('id_imagem') or imagem.get('filename') or imagem.get('id')
        else:
            filename = imagem

        if not filename:
            continue

        existente = any(item.get("id_imagem") == filename for item in related_images)
        if not existente:
            related_images.append({
                "id_imagem": filename,
                "palavras_chave": "—",
                "prob": "–",
                "relation": "Chosen by the user"
            })

    self_path = os.path.abspath(os.path.dirname(__file__))
    folder_path = os.path.join(self_path, "../frontend/public/static/InputWorks")
    process_images(folder_path, list(relatedWords))

    for item in related_images:
        if item["palavras_chave"] != "—":
            palavra_chave_imagem = item["palavras_chave"][0]
            relation = get_relation(input_words, palavra_chave_imagem, words_info)
            item["relation"] = relation  

    return list(relatedWords), related_images

