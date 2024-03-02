import streamlit as st
from simulador_entrevista import SimuladorEntrevista
import os
import openai

# Inicializa el simulador y el estado de la entrevista
if 'simulador' not in st.session_state:
    st.session_state.simulador = SimuladorEntrevista()
    st.session_state.iniciar_entrevista = False  # Estado para controlar el inicio de la entrevista

simulador = st.session_state.simulador

st.title("Simulador de Entrevistas con ChatGPT")

# Botón para comenzar la entrevista
if not st.session_state.iniciar_entrevista:
    if st.button("Iniciar Entrevista"):
        st.session_state.iniciar_entrevista = True

# Si la entrevista ha comenzado, mostrar los inputs y manejar la lógica
if st.session_state.iniciar_entrevista:
    campo = st.text_input("Introduce el campo de especialización para la entrevista:", key="campo")

    # Botón para reiniciar la entrevista completamente
    if st.button("Reiniciar Entrevista"):
        st.session_state.iniciar_entrevista = False
        st.session_state.simulador = SimuladorEntrevista()
        st.experimental_rerun()  # Esta función reinicia el script de Streamlit

    # Manejar preguntas y respuestas
    else:
        with st.form(key="pregunta_respuesta_form"):
            pregunta = st.text_input("Introduce tu pregunta para el candidato:")
            respuesta_candidato = st.text_area("Introduce la respuesta del candidato:")
            submit_button = st.form_submit_button(label="Evaluar Respuesta")

            if submit_button and pregunta and respuesta_candidato:
                # Evaluar la respuesta del candidato utilizando el modelo GPT-3.5 Turbo
                evaluacion = simulador.evaluar_respuesta_candidato(pregunta, respuesta_candidato, campo)
                st.write("Evaluación del modelo:", evaluacion)

                # Dependiendo de la evaluación, mostrar un ícono verde o rojo
                if "buena" in evaluacion.lower():  # Reemplaza con la lógica adecuada según la respuesta del modelo
                    st.markdown("🟢 La respuesta del candidato es buena según el modelo.")
                else:
                    st.markdown("🔴 La respuesta del candidato no es satisfactoria según el modelo.")

                # Limpia los campos para permitir la siguiente pregunta
                st.session_state.pregunta = ""
                st.session_state.respuesta_candidato = ""

