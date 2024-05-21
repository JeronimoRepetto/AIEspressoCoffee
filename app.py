import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import json
from transcriber import Transcriber
from llm import LLM
from weather import Weather
from tts import TTS
from pc_command import PcCommand

#Cargar llaves del archivo .env
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    #Obtener audio grabado y transcribirlo
    audio = request.files.get("audio")
    text = Transcriber(api_key=openai_api_key).transcribe(audio)
    
    llm = LLM(api_key=openai_api_key)
    function_name, args, message = llm.process_functions(text)
    if function_name is not None:
        if function_name == "get_weather":
            function_response = Weather().get(args["ubicacion"])
            function_response = json.dumps(function_response)
            print(f"Respuesta de la funcion: {function_response}")
            
            final_response = llm.process_function_response(text, message, function_name, function_response)
            tts_file = TTS(api_key=elevenlabs_key).process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "open_chrome":
            PcCommand().open_chrome(args["website"])
            final_response = "Listo, ya abrí chrome en el sitio " + args["website"]
            tts_file = TTS(api_key=elevenlabs_key).process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
    else:
        final_response =  llm.process_normal_response(text, message,)
        tts_file = TTS(api_key=elevenlabs_key).process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}
    
if __name__ == "__main__":
    app.run(debug=True)


