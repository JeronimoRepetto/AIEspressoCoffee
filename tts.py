import os
from dotenv import load_dotenv
import requests

# TODO: MIGRATE TO OPENAI
class TTS():
    def __init__(self, api_key):
        load_dotenv()
        self.key = api_key
    
    def process(self, text):
        CHUNK_SIZE = 1024
        url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"
        file_name = "response.mp3"
        file_path = os.path.join("static", file_name)

        if os.path.exists(file_path):
            print('eliminando ' + file_path)  
            os.remove(file_path)

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.key
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v1",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.55
            }
        }

        response = requests.post(url, json=data, headers=headers)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
                    
        return file_name