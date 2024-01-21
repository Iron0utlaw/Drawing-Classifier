from flask import Flask, request, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)
