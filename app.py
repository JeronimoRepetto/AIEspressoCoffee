import os
import speech_recognition as sr
import sounddevice as sd
import json
import pygame
from scipy.io.wavfile import write
from dotenv import load_dotenv
from transcriber import Transcriber
from llm import LLM
from weather import Weather
from tts import TTS
from pc_command import PcCommand

# Load keys from the .env file
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')

# Inicializar LLM una sola vez
llm = LLM(api_key=openai_api_key)

# Function to record audio
def record_audio(duration=5, sample_rate=44100):
    print("Recording audio...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()
    print("Recording complete.")
    return audio_data

# Function to save audio as WAV
def save_audio_to_wav(audio_data, filename, sample_rate=44100):
    write(filename, sample_rate, audio_data)
    print(f"Audio saved as {filename}")

# Function to transcribe audio using Whisper
def transcribe_audio(filename):
    print("Transcribing audio...")
    transcriber = Transcriber(api_key=openai_api_key)
    with open(filename, "rb") as audio_file:
        transcription = transcriber.transcribe(audio_file)
    print(f"Transcription obtained: {transcription}")
    return transcription

# Function to send text to GPT-4 and get a response
def get_gpt4_response(prompt):
    print("Getting response from GPT-4...")
    function_name, args, message = llm.process_functions(prompt)
    if function_name is not None:
        print(f"Function detected: {function_name}")
        if function_name == "get_weather":
            function_response = Weather().get(args["ubicacion"])
            function_response = json.dumps(function_response)
            final_response = llm.process_function_response(prompt, message, function_name, function_response)
            return final_response
        elif function_name == "open_chrome":
            PcCommand().open_chrome(args["website"])
            final_response = f"Done, I have opened Chrome at {args['website']}"
            return final_response
    else:
        final_response = llm.process_normal_response(prompt, message)
        return final_response

# Function to convert text to audio using ElevenLabs
def text_to_speech(text):
    print("Converting text to audio...")
    tts = TTS(api_key=elevenlabs_key)
    tts_file = tts.process(text)
    full_path = os.path.join("static", tts_file)  # Ensure we use the full path
    print(f"Audio file generated: {full_path}")
    return full_path

# Function to play the audio
def play_audio(filename):
    # Initialize pygame mixer
    pygame.mixer.init()
    if filename:
        print(f"Playing audio file: {filename}")
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            print("Playback completed.")
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error playing the audio: {e}")
    else:
        print("No audio file provided to play.")

# Main function to handle the complete logic
def handle_audio_process():
    print("Processing audio...")
    audio_data = record_audio()
    audio_filename = 'audio.wav'
    save_audio_to_wav(audio_data, audio_filename)
    transcription = transcribe_audio(audio_filename)
    if not transcription:
        print("The transcription is empty or could not be obtained.")
        return
    print(f"Transcription: {transcription}")
    response_text = get_gpt4_response(transcription)
    if not response_text:
        print("Could not get a response from GPT-4.")
        return
    print(f"Response from GPT-4: {response_text}")
    audio_file = text_to_speech(response_text)
    play_audio(audio_file)

# Voice recognizer configuration
r = sr.Recognizer()
mic = sr.Microphone()

# Listen for the activation phrase "Okey Topanga"
def main():
    print("Waiting for the activation phrase...")
    while True:
        with mic as source:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language="es-ES")
                print(f"Heard: {text}")
                if "okey topanga" in text.lower() or "okay topanga" in text.lower():
                    print("Activation phrase detected!")
                    handle_audio_process()
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError as e:
                print(f"Error requesting results; {e}")

if __name__ == "__main__":
    main()
