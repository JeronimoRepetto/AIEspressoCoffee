from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

class TTS:
    def __init__(self, api_key):
        load_dotenv()
        self.client = OpenAI(api_key=api_key)

    def process(self, text):
        file_name = "response.mp3"
        file_path = Path("static") / file_name
        if file_path.exists():
            print('Eliminando ' + str(file_path))
            file_path.unlink()

        response = self.client.audio.speech.create(
          model="tts-1",
          voice="nova",
          input=text
        )
        response.stream_to_file(file_path)
                    
        return file_name
