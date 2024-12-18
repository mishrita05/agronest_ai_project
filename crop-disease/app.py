# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# import numpy as np
# from PIL import Image
# import tensorflow as tf

# app = Flask(__name__, template_folder='templates', static_folder='static')
# CORS(app)

# # Load the pre-trained model using TFSMLayer
# MODEL = tf.keras.layers.TFSMLayer("models/1", call_endpoint='serving_default')

# CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

# @app.route('/')
# def index():
#     return render_template('index.html')

# def read_file_as_image(file) -> np.ndarray:
#     image = Image.open(file)
#     image = image.resize((256, 256))  # Resize image to the input size of the model
#     image = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
#     return image

# @tf.function
# def predict_image(image):
#     return MODEL(image)

# @app.route('/predict', methods=['POST'])
# def predict():
#     file = request.files['file']
#     if not file:
#         return jsonify({"error": "No file provided"}), 400

#     image = read_file_as_image(file)
#     img_batch = np.expand_dims(image, 0)

#     predictions = predict_image(img_batch)
#     print("Predictions:", predictions)  # Debug print

#     predicted_class = CLASS_NAMES[np.argmax(predictions['dense_1'][0])]
#     confidence = np.max(predictions['dense_1'][0]) * 100

#     return jsonify({
#         'class': predicted_class,
#         'confidence': float(confidence)
#     })

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import tensorflow as tf
from io import BytesIO

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Load the pre-trained model using TFSMLayer
MODEL = tf.keras.layers.TFSMLayer("models/1", call_endpoint='serving_default')

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

@app.route('/')
def index():
    return render_template('index.html')

def read_file_as_image(file) -> np.ndarray:
    image = np.array(Image.open(BytesIO(file.read())))
    image = image.astype('float32') / 255.0
    return image

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files["file"]
    if not file:
        return jsonify({"error": "No file provided"}), 400

    image = read_file_as_image(file.stream)
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions['dense_1'][0])]
    confidence = np.max(predictions['dense_1'][0]) * 100

    return jsonify({
        'class': predicted_class,
        'confidence': float(confidence)
    })

if __name__ == '__main__':
    app.run(debug=True)

