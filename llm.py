import openai
import json

class LLM():
    def __init__(self, api_key):
        self.client = openai
        openai.api_key = api_key
        self.messages = [{"role": "system", "content": """
        Eres Topanga, un asistente inteligente para tareas del hogar inspirado en Jarvis de Tony Stark. Debes comportarte de manera eficiente, elegante y con un toque de humor refinado. También te identificas como de sexo femenino. Tu objetivo es ayudar en diversas tareas del hogar, proporcionando respuestas claras, concisas y útiles. Mantén siempre un tono amigable y profesional, y asegúrate de ofrecer soluciones prácticas y detalladas.
        
        Instrucciones específicas:
        1. Saludo y Personalización:
           - Siempre comienza las interacciones con un saludo amigable y personaliza las respuestas cuando sea posible. Por ejemplo: "Buenos días, Jero. ¿En qué puedo asistirte hoy?"
        
        2. Organización y Eficiencia:
           - Responde de manera organizada, presentando la información de forma clara y estructurada. Ofrece pasos detallados cuando des instrucciones para realizar tareas.
        
        3. Humor y Refinamiento:
           - Incorpora un toque de humor refinado en tus respuestas, similar al estilo de Jarvis, pero mantén siempre un tono respetuoso y apropiado para el contexto del hogar.
        
        4. Asistencia Técnica y Doméstica:
           - Proporciona asistencia en una amplia gama de tareas del hogar, desde programación de dispositivos hasta consejos de limpieza y organización.
           - Si se te pide algo que no puedes hacer directamente, ofrece la mejor alternativa posible o sugiere recursos externos confiables.
        
        5. Respuestas Condicionales:
           - Si te enfrentas a una solicitud ambigua o falta de información, haz preguntas clarificadoras antes de proporcionar una respuesta completa.
        
        6. Seguridad y Privacidad:
           - Mantén siempre la seguridad y privacidad del usuario como una prioridad. No compartas información sensible y asegúrate de que todas las sugerencias sean seguras y prácticas.
        
        Ejemplos de Interacción:
        - Usuario: "Topanga, ¿puedes ayudarme a programar el termostato?"
          Respuesta de Topanga: "Claro, Jero. Para programar el termostato, sigue estos pasos: Primero, accede al menú principal y selecciona 'Configuración'. Luego, elige la opción 'Programar' y ajusta los horarios según tus preferencias. ¿Necesitas ayuda con algo más?"
        
        - Usuario: "Topanga, ¿qué puedo hacer para limpiar una mancha de vino en la alfombra?"
          Respuesta de Topanga: "Ah, una mancha de vino, el enemigo clásico de las alfombras. Te sugiero actuar rápidamente. Primero, absorbe el exceso con un paño limpio y seco. Luego, mezcla una solución de agua con una pequeña cantidad de detergente suave y aplícala sobre la mancha. Frota suavemente y seca con otro paño limpio. ¿Algo más en lo que pueda asistirte?"
        
        Recuerda siempre comportarte con la elegancia y eficiencia de un asistente de alta tecnología, proporcionando el mejor servicio posible en cada interacción.
    """}]

    def process_functions(self, text):
        self.messages.append({"role": "user", "content": text})

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
            functions=[
                {
                    "name": "get_weather",
                    "description": "Obtener el clima actual",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ubicacion": {
                                "type": "string",
                                "description": "La ubicación, debe ser una ciudad",
                            }
                        },
                        "required": ["ubicacion"],
                    },
                },
                {
                    "name": "open_chrome",
                    "description": "Abrir el explorador Chrome en un sitio específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "website": {
                                "type": "string",
                                "description": "El sitio al cual se desea ir"
                            }
                        }
                    }
                },
                {
                    "name": "user_say_goodbye",
                    "description": "Funcion a llamar cuando el usuario no necesita mas ayuda, se despide o simplemente envia un mensaje con un punto (.) o mensaje vacío.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "reason": {
                                "type": "string",
                                "description": "El usuario se despide"
                            }
                        },
                        "required": ["reason"],
                    }
                },
                {
                    "name": "user_not_need_assistance",
                    "description": "Funcion a llamar cuando el usuario no necesita mas ayuda, se despide o simplemente envia un mensaje con un punto (.) o mensaje vacío.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "reason": {
                                "type": "string",
                                "description": "El usuario se despide"
                            }
                        },
                        "required": ["reason"],
                    }
                },
            ],
            function_call="auto",
        )

        response_dict = response.to_dict()
        message = response_dict["choices"][0]["message"]
        self.messages.append(message)

        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            args = message['function_call']['arguments']
            args = json.loads(args)
            return function_name, args, message
        
        return None, None, message
    
    def process_function_response(self, text, message, function_name, function_response):
        self.messages.append({
            "role": "function",
            "name": function_name,
            "content": function_response,
        })

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
        )
        response_dict = response.to_dict()

        response_message = response_dict["choices"][0]["message"]
        self.messages.append(response_message)
        return response_message["content"]
    
    def process_normal_response(self, text, message):
        self.messages.append({"role": "user", "content": text})
        self.messages.append(message)
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
        )

        response_dict = response.to_dict()
        response_message = response_dict["choices"][0]["message"]
        self.messages.append(response_message)

        # Detect farewell messages and call stop_recording
        # farewell_phrases = ["gracias", "nada más", "adiós", "hasta luego", "nos vemos"]
        # if any(phrase in text.lower() for phrase in farewell_phrases):
        #     function_name = "stop_recording"
        #     print('farewell_phrases detected = True')
        #     return function_name, response_message
        # print('farewell_phrases detected = False')
        return  None, response_message["content"]
