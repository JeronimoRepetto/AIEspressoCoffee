from openai import OpenAI

class Transcriber:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def transcribe(self, audio_file):
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcript.text