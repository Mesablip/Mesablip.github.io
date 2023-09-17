from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from flask_cors import cross_origin
from PIL import Image, ImageOps
import io
import json
import requests
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key'

CORS(app)

UPLOAD_FOLDER = 'data'

@app.route('/')
@cross_origin()
def index():
    return render_template('frontend.html')

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    #user_id = request.form.get('user_id')
    game_id = request.form.get('game_id')
    uploaded_files = request.files.getlist('photos')
    file_paths = []

    for i, file in enumerate(uploaded_files):
        file_name = f"temp_image_{i}.jpg"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        file.save(file_path)
        file_paths.append(file_name)
        """# Convert the uploaded file to a PIL Image object
        image = Image.open(io.BytesIO(file.read()))
        
        # Perform the image transformations here
        fixed_image = ImageOps.exif_transpose(image)
        
        byte_arr = io.BytesIO()

        fixed_image.save(byte_arr, format='JPEG')
        byte_arr.seek(0)

        files = {"backgroundPicture": ("279EF96B-957C-4E96-BF86-273586D3B112.JPG", byte_arr, "image/jpeg")}
        post_data = json.loads(requests.get(f'https://scorestream.com/api?request=%7B%22method%22:%22games.posts.add%22,%22params%22:%7B%22accessToken%22:%2267556df4-85ad-48f3-8e51-418a9d5af78d%22,%22gameId%22:{game_id},%22userText%22:%22Hey%22%7D%7D', files=files).text)
        print(post_data)"""

    with open("temp_file_paths.txt", "w") as f:
        f.write(json.dumps(file_paths))
    
    with open("game_id.txt", "w") as f:
        f.write(json.dumps(game_id))

    return render_template('caption.html')

@app.route('/save_captions', methods=['POST'])
@cross_origin()
def save_captions():
    data = request.get_json()
    captions = data.get('captions', [])
    print(captions)

    with open("temp_file_paths.txt", "r") as f:
        file_paths = json.loads(f.read())

    with open("game_id", "r") as f:
        game_id = json.loads(f.read())[0]

    # Now you have `captions` list and `file_paths` list
    # You can process them together based on their index
    for i in range(len(captions)):
        with open("data\\" + file_paths[i], "rb") as f:
            image = Image.open(io.BytesIO(f.read()))

            # Perform the image transformations here
            fixed_image = ImageOps.exif_transpose(image)

            byte_arr = io.BytesIO()

            fixed_image.save(byte_arr, format='JPEG')
            byte_arr.seek(0)

            files = {"backgroundPicture": ("279EF96B-957C-4E96-BF86-273586D3B112.JPG", byte_arr, "image/jpeg")}

            post_data = json.loads(requests.get(f'https://scorestream.com/api?request=%7B%22method%22:%22games.posts.add%22,%22params%22:%7B%22accessToken%22:%2267556df4-85ad-48f3-8e51-418a9d5af78d%22,%22gameId%22:{game_id},%22userText%22:%22{captions[i]}%22%7D%7D', files=files).text)
            print(post_data)
        print(f"Caption for {file_paths[i]} is {captions[i]}")

    # You can also save them to database, or further process them here...

    return jsonify({"message": "Captions received"})

@app.route('/caption', methods=['GET'])
@cross_origin()
def caption_images():
    with open("temp_file_paths.txt", "r") as f:
        file_paths = json.loads(f.read())
    return render_template('caption.html', file_paths=file_paths)

@app.route('/send_file/<path:filename>', methods=['GET'])
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
if __name__ == '__main__':
    app.run(debug=True)
