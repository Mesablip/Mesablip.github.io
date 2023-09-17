from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageOps
import io
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    #user_id = request.form.get('user_id')
    uploaded_files = request.files.getlist('photos')
    
    for file in uploaded_files:
        # Convert the uploaded file to a PIL Image object
        image = Image.open(io.BytesIO(file.read()))
        
        # Perform the image transformations here
        fixed_image = ImageOps.exif_transpose(image)
        
        byte_arr = io.BytesIO()

        fixed_image.save(byte_arr, format='JPEG')
        byte_arr.seek(0)

        files = {"backgroundPicture": ("279EF96B-957C-4E96-BF86-273586D3B112.JPG", byte_arr, "image/jpeg")}
        post_data = json.loads(requests.get('https://scorestream.com/api?request=%7B%22method%22:%22games.posts.add%22,%22params%22:%7B%22accessToken%22:%221d9d5d16-9e63-4be9-9962-bc9fefe23083%22,%22gameId%22:4694439,%22userText%22:%22Hey%22%7D%7D', files=files).text)
        print(post_data)
    return jsonify({"message": "Files processed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)