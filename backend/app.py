from flask import Flask, request, jsonify, send_from_directory, session, current_app 
from flask_cors import CORS

from loadImages import get_images_data
from select_images import find_related_images, related_images
from unit import setting_up_solutions
from decompose import decompose
from llama import llama_model
from expand import generating
import os
import json
import base64
import shutil

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(
    __name__,
    static_folder=os.path.join(project_root, 'frontend', 'public'),
    template_folder=os.path.join(project_root, 'frontend', 'public'),
    static_url_path=''  
)

CORS(app, resources={r"/*": {"origins": "*"}})

population = None
archive = None
counter = 0

population_pattern = None
archive_pattern = None

self_path = os.path.abspath(os.path.dirname(__file__))
app.secret_key = '123'



@app.route('/api/images', methods=['GET'])
def get_all_images():
    try:
        images = get_images_data()
        return jsonify({"images": images})  
    except Exception as e:
        print("Error fetching images:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/receber-dados', methods=['GET'])
def receber_dados():
    try:
        inputword = request.args.get('inputword', '')
        userSelectedImages = request.args.get('userSelectedImages', '[]')
        userSelectedImages = json.loads(userSelectedImages)   
        relatedWords, related_images = find_related_images(inputword, userSelectedImages)
        if not isinstance(relatedWords, list) or not isinstance(related_images, list):
            raise ValueError("Processing error: relatedWords or related_images is not a list.")

        return jsonify({
            "success": True,
            "searchTerm": inputword,
            "relatedWords": relatedWords,
            "selectedImages": related_images,
        })
    except Exception as e:
        print("Error /receber-dados:", e)
        return jsonify({"success": False, "message": str(e)}), 500
 
@app.route('/selectedGallery')
def selected_gallery():
    return "", 204  

@app.route('/decompor', methods=['GET'])
def decompor(): 
    semanticWords = request.args.get('semanticWords')
    searchTerm = request.args.get('searchTerm')
    selectImages = request.args.get('selectImages')
    selected_images = json.loads(selectImages)

    png_files, png_files_name, decomposed_info = decompose(selected_images, searchTerm, semanticWords)

    clear_directory(os.path.join(project_root, "frontend", "public", "static", 'final_unit'))
    clear_directory(os.path.join(project_root, "backend", "static", 'final_unit'))
    clear_directory(os.path.join(project_root, "frontend", "public", "static", 'temp_unit'))
    clear_directory(os.path.join(project_root, "frontend", "public", "static", 'elements_png'))
    clear_directory(os.path.join(project_root, "frontend", "public", "static", 'elements_png_name'))


    backend_png_dir = os.path.join(project_root, 'backend', 'static', 'elements_png')

    frontend_png_dir = os.path.join(project_root, "frontend", "public", "static", 'elements_png')

    if os.path.exists(backend_png_dir):
        for filename in os.listdir(backend_png_dir):
            src_file = os.path.join(backend_png_dir, filename)
            dest_file = os.path.join(frontend_png_dir, filename)
            if os.path.isfile(src_file):
                shutil.copy(src_file, dest_file)

    return jsonify({"success": True, 
                    "message": "Decomposition successfully completed!",
                    "png_files": png_files,
                    "searchTerm": searchTerm,
                    "relatedWords": semanticWords,
                    "png_files_name": png_files_name,
                    "decomposed_info": decomposed_info}), 200

@app.route('/static/<path:filename>')
def serve_static(filename):
    static_path = os.path.join(project_root, 'frontend', 'public', 'static')
    return send_from_directory(static_path, filename)

@app.route("/api/initial-solutions", methods=["GET"])
def get_initial_solutions():
    solutions = setting_up_solutions()

    return jsonify({"solutions": solutions})

def clear_directory(directory):
    os.makedirs(directory, exist_ok=True) 
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                clear_directory(file_path)
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

@app.route('/wordDefinition', methods=['GET'])
def word_definition():
    keyword = request.args.get('keyword')
    relation = request.args.get('relation')
    definition = llama_model(keyword, relation)
    return jsonify({"definition": definition})


@app.route("/api/expand-pattern", methods=["POST"])
def expand_pattern():
    try:
        data = request.get_json()
        canvas_data = data.get("canvasData")
        imagesInfo = data.get("imagesInfo")
        output_filepath = os.path.join(project_root, "backend", "static", "expand_pattern", "my_custom_pattern.png")
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

        generating(canvas_data, imagesInfo, output_filepath)

        if not canvas_data:
            return jsonify({"success": False, "message": "Canvas data is required."}), 400

        
        return jsonify({"success": True, "message": "Pattern expanded successfully.", "patternPath": output_filepath}), 200
    except Exception as e:
        print(f"Error in expand_pattern: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/backend/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/api/save_canvas', methods=['POST'])
def save_canvas():
    elements_path_backend = os.path.join(project_root, "backend", "static", "final_unit")
    os.makedirs(elements_path_backend, exist_ok=True)
    elements_path = os.path.join(project_root, "frontend", "public", "static", "final_unit")
    os.makedirs(elements_path, exist_ok=True)
    data = request.json
    image_data = data.get('imageData')
    file_name = data.get('fileName', 'output.png')

    if not image_data or not file_name:
        return {"error": "Invalid data!"}, 400

    if image_data.startswith('data:image/png;base64,'):
        image_data = image_data.split(',', 1)[1]

    file_path = os.path.join(elements_path, file_name)
    file_path_backend = os.path.join(elements_path_backend, file_name)
    try:
        decoded_data = base64.b64decode(image_data)
        
        with open(file_path, 'wb') as f:
            f.write(decoded_data)
            f.flush()           
            os.fsync(f.fileno()) 

        with open(file_path_backend, 'wb') as f:
            f.write(decoded_data)
            f.flush()
            os.fsync(f.fileno())

        return jsonify({"success": True, "message": "Saved successfully", "path": f"/static/final_unit/{file_name}"})
        
    except Exception as e:
        print(f"Error saving canvas: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route("/api/save_final_pattern", methods=["POST"])
def save_final_pattern():
    try:
        data = request.json
        image_data = data.get("imageData")

        if not image_data:
            return jsonify({"success": False, "message": "No image received"}), 400

        if image_data.startswith("data:image/png;base64,"):
            image_data = image_data.split(",", 1)[1]
        
        decoded_data = base64.b64decode(image_data)

        waiting_dir = os.path.join(project_root, "frontend", "public", "static", "waitingGallery")
        final_pattern_dir = os.path.join(project_root, "frontend", "public", "static", "final_pattern")

        os.makedirs(waiting_dir, exist_ok=True)
        os.makedirs(final_pattern_dir, exist_ok=True)

        existing_files = os.listdir(waiting_dir)
        
        max_number = -1
        
        for f in existing_files:
            name_part = os.path.splitext(f)[0]
            if name_part.isdigit():
                num = int(name_part)
                if num > max_number:
                    max_number = num
        
        next_number = max_number + 1
        new_filename = f"{next_number}.png"
        
        waiting_path = os.path.join(waiting_dir, new_filename)
        final_pattern_path = os.path.join(final_pattern_dir, new_filename)

        with open(waiting_path, "wb") as f:
            f.write(decoded_data)
            f.flush()
            os.fsync(f.fileno())  
    
        with open(final_pattern_path, "wb") as f:
            f.write(decoded_data)
            f.flush()
            os.fsync(f.fileno())
        return jsonify({
            "success": True, 
            "path": f"/static/final_pattern/{new_filename}",
            "filename": new_filename
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/waiting-gallery', methods=['GET'])
def get_waiting_gallery_images():
    try:
        waiting_dir = os.path.join(project_root, "frontend", "public", "static", "waitingGallery")
        
        if not os.path.exists(waiting_dir):
            os.makedirs(waiting_dir)
            return jsonify({"images": []})

        valid_extensions = ('.png', '.jpg', '.jpeg', '.svg')
        
        files = [f for f in os.listdir(waiting_dir) if f.lower().endswith(valid_extensions)]
        
        return jsonify({"images": files})
    except Exception as e:
        print(f"Error reading waiting gallery: {e}")
        return jsonify({"images": []}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)



