from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from PIL import Image, ImageOps
import io
import json
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'path/to/upload/folder'

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    #user_id = request.form.get('user_id')
    game_id = request.form.get('game_id')
    uploaded_files = request.files.getlist('photos')
    file_paths = []

    for i, file in enumerate(uploaded_files):
        image_bytes = file.read()
        image_list.append(image_bytes)
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
    session["images"] = image_list
    return redirect(url_for("caption_images"))

@app.route('/caption', methods=['GET'])
def caption_images():
    image_list = session.get('images', [])
    return render_template('caption.html', images=image_list)

if __name__ == '__main__':
    app.run(debug=True)