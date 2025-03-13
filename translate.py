from googletrans import Translator
from gtts import gTTS
import os

# Supported languages
LANGUAGES = {
    'hi': 'Hindi',
    'mr': 'Marathi',
    'pa': 'Punjabi',
    'te': 'Telugu',
    'ta': 'Tamil',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'gu': 'Gujarati',
    'bn': 'Bengali'
}

def translate_and_speak(text, lang_code):
    if lang_code not in LANGUAGES:
        print("Invalid language code! Choose from:", LANGUAGES)
        return

    # Translate English to chosen language
    translator = Translator()
    translated = translator.translate(text, src='en', dest=lang_code)
    translated_text = translated.text
    print(f"Translated ({LANGUAGES[lang_code]}): {translated_text}")

    # Convert text to speech
    tts = gTTS(text=translated_text, lang=lang_code)
    filename = f"output_{lang_code}.mp3"
    tts.save(filename)
    os.system(f"mpg321 {filename}")  # Play audio (use any player)

# User input
english_text = input("Enter text in English: ")
print("Available Languages:", LANGUAGES)
chosen_lang = input("Enter language code (e.g., 'hi' for Hindi, 'mr' for Marathi): ").strip()

# Translate & Speak
translate_and_speak(english_text, chosen_lang)
