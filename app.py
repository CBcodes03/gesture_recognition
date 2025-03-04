from flask import Flask, render_template, request, url_for, jsonify
import os
import cv2
import mediapipe as mp
import base64
import numpy as np
import time
from predict import predict_sentence
app = Flask(__name__)

# Paths for ASL and ISL image folders
ASL_PATH = "static/ASL"
ISL_PATH = "static/ISL"
DETECTED_TEXT=''

# Function to translate text into sign language images
def get_sign_language_images(text, language):
    folder_path = ASL_PATH if language == "ASL" else ISL_PATH
    images = []
    for letter in text.lower():
        if letter.isalpha() or letter.isdigit():
            image_filename = f"{letter}.jpg"
            image_path = os.path.join(folder_path, image_filename)
            if os.path.exists(image_path):
                image_url = url_for('static', filename=f"{language.upper()}/{image_filename}")
                images.append(image_url)
            else:
                images.append(url_for('static', filename="placeholder.jpg"))
    return images

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Global variable to store detected gesture
recognizer_detected = None

# Output function for gesture recognition
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global recognizer_detected
    if result.gestures and len(result.gestures) > 0 and len(result.gestures[0]) > 0:
        recognizer_detected = result.gestures[0][0].category_name
        print('Gesture Recognition Result:', recognizer_detected)
    else:
        recognizer_detected = None

# Setting options for gesture recognition
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='exported_models/gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

recognizer = GestureRecognizer.create_from_options(options)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'GET':
        return render_template('trans.html')

    # Handle POST request
    text_input = request.form.get("text_input")
    speech_input = request.form.get("speech_input")
    language_choice = request.form.get("language")

    input_text = text_input if text_input else speech_input

    if input_text:
        images = get_sign_language_images(input_text, language_choice)
        return render_template('trans.html', images=images, input_text=input_text, language=language_choice)

    return render_template('trans.html', images=None)

@app.route('/process_frame', methods=['GET','POST'])
def process_frame():
    global DETECTED_TEXT
    if request.method == 'GET':
        return render_template('index.html')
    global recognizer_detected
    frame_timestamp_ms = int(time.time() * 1000)

    # Get the image data from the request
    data = request.json
    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)

    np_array = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Process the frame for gesture recognition
    recognizer.recognize_async(mp_image, frame_timestamp_ms)

    # Process hand landmarks
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display recognized gesture on the frame
    if recognizer_detected:
        cv2.putText(frame, recognizer_detected, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)
        DETECTED_TEXT=DETECTED_TEXT+recognizer_detected

    # Encode processed image for response
    ret, buffer = cv2.imencode('.jpg', frame)
    processed_image = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify(result=recognizer_detected, image='data:image/jpeg;base64,' + processed_image)

@app.route('/predict', methods=['POST'])
def P_text():
    global DETECTED_TEXT
    if len(DETECTED_TEXT) > 0:
        temp = DETECTED_TEXT
        DETECTED_TEXT=''
        temp=predict_sentence(temp)
        print(temp)
        return jsonify(prediction=temp)
    else:
        return jsonify(prediction="No gestures recognized")

if __name__ == '__main__':
    app.run(debug=True)
