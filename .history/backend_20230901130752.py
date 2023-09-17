from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageOps
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('frontend.html')

"""@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_files = request.files.getlist('photos')
    
    for file in uploaded_files:
        # Convert the uploaded file to a PIL Image object
        image = Image.open(io.BytesIO(file.read()))
        
        # Perform the image transformations here
        fixed_image = ImageOps.exif_transpose(image)
        
        # Your other code to further process and maybe upload the image somewhere

    return jsonify({"message": "Files processed successfully"}), 200
"""
if __name__ == '__main__':
    app.run(debug=True)