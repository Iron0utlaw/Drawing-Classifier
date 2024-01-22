from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import cv2 as cv
import numpy as np
from sklearn.svm import LinearSVC


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

a = 0
b = 0
c = 0
clf = LinearSVC()

def get_folder_name(route):
    return os.path.join(app.config['UPLOAD_FOLDER'], route)

def generate_unique_filename(subfolder):
    global a, b, c
    if subfolder == 'A':
        a += 1
        return f"image_{a}.png"
    elif subfolder == "B":
        b += 1
        return f"image_{b}.png"
    elif subfolder == "C":
        c += 1
        return f"image_{c}.png"
    else: return f"image.png"

@app.route('/uploadA', methods=['POST'])
def upload_image_A():
    return upload_image('A')

@app.route('/uploadB', methods=['POST'])
def upload_image_B():
    return upload_image('B')

@app.route('/uploadC', methods=['POST'])
def upload_image_C():
    return upload_image('C')

@app.route('/upload_pred', methods=['POST'])
def upload_image_pred():
    return upload_image('pred')

def upload_image(subfolder):
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected image file'}), 400

    folder = get_folder_name(subfolder)
    os.makedirs(folder, exist_ok=True)

    filename = os.path.join(folder, generate_unique_filename(subfolder))
    image.save(filename)
    return jsonify({'imageUrl': filename})


@app.route('/train')
def train():
    global a, b, c, clf

    img_list = np.array([])
    class_list = np.array([])
    print(a,b,c)

    for x in range(1, a + 1):
        img = cv.imread(f"{UPLOAD_FOLDER}/A/image_{x}.png")[:, :, 0]
        img = img.reshape(250000)
        img_list = np.append(img_list, [img])
        class_list = np.append(class_list, 1)

    for x in range(1, b + 1):
        img = cv.imread(f"{UPLOAD_FOLDER}/B/image_{x}.png")[:, :, 0]
        img = img.reshape(250000)
        img_list = np.append(img_list, [img])
        class_list = np.append(class_list, 2)

    for x in range(1, c + 1):
        img = cv.imread(f"{UPLOAD_FOLDER}/C/image_{x}.png")[:, :, 0]
        img = img.reshape(250000)
        img_list = np.append(img_list, [img])
        class_list = np.append(class_list, 3)

    img_list = img_list.reshape(a + b + c, 250000)

    clf.fit(img_list, class_list)
    
    return jsonify({'status': "OK"})

@app.route('/')
def home():
    return "Backend Live"

@app.route('/pred')
def pred():
    global clf
    img = cv.imread(f"{UPLOAD_FOLDER}/pred/image.png")[:, :, 0]
    img = img.reshape(250000)
    prediction = clf.predict([img])
    
    if prediction[0] == 1:
        return jsonify({'status': "A"})
    elif prediction[0] == 2:
        return jsonify({'status': "B"})
    elif prediction[0] == 3:
        return jsonify({'status': "C"})

if __name__ == '__main__':
    app.run(debug=True)