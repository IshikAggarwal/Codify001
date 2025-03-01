from flask import Flask, request, jsonify
import cv2
import numpy as np
from DeepFace import DeepFace
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_deepfake(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return "No Face Detected"

    for (x, y, w, h) in faces:
        face_roi = image[y:y+h, x:x+w]

        # DeepFace face analysis (Emotion consistency check)
        try:
            analysis = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
            emotion = analysis[0]['dominant_emotion']
            if emotion in ["neutral", "happy", "surprise"]:
                return "Real"
            else:
                return "Fake"
        except:
            return "Error analyzing face"

    return "Real"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    prediction = detect_deepfake(file_path)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
