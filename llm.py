from openai import OpenAI
import json

#Clase para utilizar cualquier LLM para procesar un texto
#Y regresar una funcion a llamar con sus parametros
#Uso el modelo 0613, pero puedes usar un poco de
#prompt engineering si quieres usar otro modelo
class LLM():
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def process_functions(self, text):
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                    {"role": "system", "content": "Eres un asistente multitarea tu nombre es Topanga y eres cordial conmigo, Jeronimo, tu creador."},
                    {"role": "user", "content": text},
            ], functions=[
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
                # {
                #     "name": "send_email",
                #     "description": "Enviar un correo",
                #     "parameters": {
                #         "type": "object",
                #         "properties": {
                #             "recipient": {
                #                 "type": "string",
                #                 "description": "La dirección de correo que recibirá el correo electrónico",
                #             },
                #             "subject": {
                #                 "type": "string",
                #                 "description": "El asunto del correo",
                #             },
                #             "body": {
                #                 "type": "string",
                #                 "description": "El texto del cuerpo del correo",
                #             }
                #         },
                #         "required": [],
                #     },
                # },
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
            ],
            function_call="auto",
        )
        
        response_dict = response.to_dict()
        message = response_dict["choices"][0]["message"]

        print('----------------------------------------------')
        print('----------------------------------------------')
        print(message)
        print('----------------------------------------------')
        print('----------------------------------------------')
        print(message.get("function_call"))
        print('----------------------------------------------')
        print('----------------------------------------------')

        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            args = message['function_call']['arguments']
            print("Funcion a llamar: " + function_name)
            args = json.loads(args)
            return function_name, args, message
        
        return None, None, message
    
    #Una vez que llamamos a la funcion (e.g. obtener clima, encender luz, etc)
    #Podemos llamar a esta funcion con el msj original, la funcion llamada y su
    #respuesta, para obtener una respuesta en lenguaje natural (en caso que la
    #respuesta haya sido JSON por ejemplo
    def process_function_response(self, text, message, function_name, function_response):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                #Aqui tambien puedes cambiar como se comporta
                {"role": "system", "content": "Eres un asistente multitarea tu nombre es Topanga y eres cordial conmigo, Jeronimo, tu creador."},
                {"role": "user", "content": text},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        response_dict = response.to_dict()
        return response_dict["choices"][0]["message"]["content"]
    
    def process_normal_response(self, text, message):
     response = self.client.chat.completions.create(
         model="gpt-4o",
         messages=[
             #Aqui tambien puedes cambiar como se comporta
             {"role": "system", "content": "Eres un asistente multitarea tu nombre es Topanga y eres cordial conmigo, Jeronimo, tu creador."},
             {"role": "user", "content": text},
             message,
         ],
     )
     response_dict = response.to_dict()
     return response_dict["choices"][0]["message"]["content"]