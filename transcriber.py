from openai import OpenAI
class Transcriber:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    #Siempre guarda y lee del archivo audio.mp3
    #Utiliza whisper en la nube :) puedes cambiarlo por una impl local
    def transcribe(self, audio):
        audio.save("audio.mp3")
        audio_file= open("audio.mp3", "rb")
        transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
        return transcript.text