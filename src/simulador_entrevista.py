from config import decorador_tiempo, inicializar_api_openai, logging
import openai


# Clase SimuladorEntrevista actualizada para integrar ChatGPT
class SimuladorEntrevista:
    def __init__(self):
        inicializar_api_openai()  # Inicializa la clave API al instanciar la clase
        self.historial_conversacion = []  # Almacena el historial de la conversación

    @decorador_tiempo
    def obtener_respuesta_candidato(self, pregunta, campo):
        """Obtiene la respuesta del modelo (candidato) a una pregunta de entrevista manteniendo el contexto."""
        self.historial_conversacion.append({"role": "user", "content": pregunta})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.historial_conversacion
            )
            respuesta = response.choices[0].message['content'].strip()
            self.historial_conversacion.append(
                {"role": "assistant", "content": respuesta})  # Añade la respuesta al historial

            logging.info(f"Respuesta del candidato en {campo}: {respuesta}")
            return respuesta
        except Exception as e:
            logging.error(f"Error al obtener respuesta: {e}")
            return "Hubo un error al procesar la pregunta, por favor intenta nuevamente."

    def iniciar_entrevista(self):
        campo_actual = input("Introduce el campo de especialización para la entrevista: ")
        self.historial_conversacion.append(
            {"role": "system", "content": f"Esta es una entrevista en el campo de {campo_actual}."})

        print(f"\nVamos a comenzar la entrevista sobre {campo_actual}.\n")

        continuar = 's'
        while continuar.lower() == 's':
            pregunta = input("\nIntroduce tu pregunta: ")
            respuesta = self.obtener_respuesta_candidato(pregunta, campo_actual)
            print(f"\nRespuesta del candidato: {respuesta}")

            continuar = input("\n¿Deseas hacer otra pregunta? (s/n): ")
        logging.info("Entrevista finalizada.")

    def registrar_respuesta(self, pregunta, respuesta):
        # Registra la pregunta como un mensaje del usuario
        self.historial_conversacion.append({"role": "user", "content": pregunta})
        # Registra la respuesta como un mensaje del sistema o asistente
        self.historial_conversacion.append({"role": "assistant", "content": respuesta})

    def evaluar_respuesta_candidato(self, pregunta, respuesta_candidato, campo):
        """
        Evalúa la respuesta del candidato utilizando GPT-3.5 Turbo.
        Se asume que el modelo está entrenado para proporcionar una evaluación basada en una respuesta dada.
        """
        # Prepara los mensajes para la conversación
        messages = [
            {"role": "system", "content": f"Esta es una entrevista en el campo de {campo}."},
            {"role": "user", "content": f"Pregunta: {pregunta}\nRespuesta: {respuesta_candidato}"}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            evaluacion = response.choices[0].message['content'].strip()
            return evaluacion
        except Exception as e:
            logging.error(f"Error al evaluar la respuesta del candidato: {e}")
            return "No se pudo procesar la evaluación, intenta de nuevo."