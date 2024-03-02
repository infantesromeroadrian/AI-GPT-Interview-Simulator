import logging
import openai
import time
import os

# Configuración inicial del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Decorador para medir y registrar el tiempo de ejecución de las funciones
def decorador_tiempo(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        logging.info(f"{func.__name__} ha tardado {fin - inicio} segundos en ejecutarse.")
        return resultado
    return wrapper

def inicializar_api_openai():
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if openai.api_key is None:
            raise ValueError("La clave API de OpenAI no está configurada como variable de entorno.")
    except Exception as e:
        logging.error("Error al inicializar la clave API de OpenAI: " + str(e))
        raise
