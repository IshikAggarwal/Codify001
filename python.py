from flask import Flask, request, jsonify
import base64
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf  # Example ML framework

app = Flask(__name__)

# Load your ML model (replace with your actual model)
model = tf.keras.models.load_model('ai_detection_model.h5')

def preprocess_image(base64_image):
    # Decode Base64 image
    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))
    image = image.resize((224, 224))  # Resize to model's input size
    image = np.array(image) / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

@app.route('/detect', methods=['POST'])
def detect():
    data = request.json
    base64_image = data['image']
    image = preprocess_image(base64_image)
    
    # Predict using the ML model
    prediction = model.predict(image)
    result = "AI-generated" if prediction[0] > 0.5 else "Not AI-generated"
    
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)