import streamlit as st
import openai
import os
from dotenv import load_dotenv
import whisper

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de la API key desde las variables de entorno
api_key = os.getenv("OPEN_AI_API_KEY")

# Configurar la API de OpenAI
openai.api_key = api_key

#Se carga el modelo de transcripcion
def load_whisper_model():
    try:
        model = whisper.load_model("base")
        return model
    except Exception as e:
        st.error(f"Error loading Whisper model: {e}")
        return None
#Funcion para transcribir el audio
def transcribe_audio(model, file_path):
    try:
        transcript = model.transcribe(file_path)
        return transcript['text']
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return ""

#Configuracion del chatbot
def custom_chatgpt(user_input):
    messages = [{"role": "system", "content": "You are an office administrator, summarize the text in key points"}]
    messages.append({"role": "user", "content": user_input})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        chatgpt_reply = response["choices"][0]["message"]["content"]
        return chatgpt_reply
    except Exception as e:
        st.error(f"Error in ChatGPT response: {e}")
        return ""

# Programa principal
model = load_whisper_model()
if model:
    st.title("Transcripción y Resumen de Audio")
    option = st.selectbox("Seleccione una opción:", ("Cargar archivo personalizado", "Transcribir archivo demo"))
    
    if option == "Cargar archivo personalizado":
        uploaded_file = st.file_uploader("Seleccione un archivo de audio", type=['mp3', 'wav', 'm4a'])
        if uploaded_file is not None:
            with open("temp_audio_file", "wb") as f:
                f.write(uploaded_file.getbuffer())
            custom_transcription = transcribe_audio(model, "temp_audio_file")
            st.text("Transcripción:")
            st.text(custom_transcription)
            st.text("#######################################")
            custom_summary = custom_chatgpt(custom_transcription)
            st.text("Resumen:")
            st.text(custom_summary)
    
    elif option == "Transcribir archivo demo":
        file_path = 'MA1.m4a'
        transcription = transcribe_audio(model, file_path)
        st.text("Transcripción:")
        st.text(transcription)
        st.text("#######################################")
        summary = custom_chatgpt(transcription)
        st.text("Resumen:")
        st.text(summary)
