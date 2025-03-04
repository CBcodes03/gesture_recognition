# Gesture Recognition and Sign Language Translator

This project is an **AI-based gesture recognition tool** that translates sign language into text. It captures gestures from a webcam, processes the frames, and predicts the corresponding text.

## Features
- **Real-time Gesture Recognition:** Uses a webcam to capture hand gestures.
- **AI-powered Prediction:** Processes frames and predicts the sign language translation.
- **Start/Stop Camera:** Controls for enabling and disabling gesture recognition.
- **Text Prediction:** Converts recognized gestures into readable text.
- **Automatic UI Updates:** Disables prediction while capturing is active.

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **AI Model:** Google Gemini API (Gemini-2.0 Flash)

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/gesture_recognition.git . (some folder)
   cd (folder name)
   ```
2. **Create a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up the API Key:**
   - Replace `api_key` in `predict_sentence` function with your Google Gemini API key.

## Running the Project
1. **Start the Flask server:**
   ```sh
   python app.py
   ```
2. **Open the application in your browser:**
   ```
   http://127.0.0.1:5000
   ```

## Usage
1. Click **"Start Gesture Recognition"** to enable the webcam.
2. Perform gestures in front of the camera.
3. Click **"Predict"** to convert gestures into text.
4. Click **"Stop Gesture Recognition"** to disable the camera and reset the output.


## Future Enhancements
- Add support for more sign languages.
- Improve accuracy using advanced AI models.
- Implement voice output for translations.

---
Feel free to contribute or report issues!

