from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected image file'}), 400

    # Ensure the 'uploads' directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.png')
    image.save(filename)

    # Your additional processing logic here

    return jsonify({'imageUrl': filename})

@app.route('/get_uploaded_image', methods=['GET'])
def get_uploaded_image():
    # Return the saved image to the client
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.png')
    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
