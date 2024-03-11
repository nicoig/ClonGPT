# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git remote add origin https://github.com/nicoig/jacobo-grinberg-ia.git
# git commit -m "Initial commit"
# git push -u origin master

# Actualizar Repo de Github
# git add .
# git commit -m "Se actualizan las variables de entorno"
# git push origin master

# En Render
# agregar en variables de entorno
# PYTHON_VERSION = 3.9.12

################################################



import streamlit as st
import time
import base64
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Set your OpenAI API key and assistant ID here
api_key = os.getenv("OPENAI_APIKEY")
assistant_id = os.getenv("ASSISTANT_ID")

# Set openAi client, assistant ai and assistant ai thread
@st.cache_resource
def load_openai_client_and_assistant():
    client = OpenAI(api_key=api_key)
    my_assistant = client.beta.assistants.retrieve(assistant_id)
    thread = client.beta.threads.create()
    return client, my_assistant, thread

client, my_assistant, assistant_thread = load_openai_client_and_assistant()

# Check in loop if assistant ai parse our request
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(0.5)
    return run

# Initiate assistant ai response
def get_assistant_response(user_input=""):
    message = client.beta.threads.messages.create(thread_id=assistant_thread.id, role="user", content=user_input)
    run = client.beta.threads.runs.create(thread_id=assistant_thread.id, assistant_id=assistant_id)
    run = wait_on_run(run, assistant_thread)
    messages = client.beta.threads.messages.list(thread_id=assistant_thread.id, order="asc", after=message.id)
    return messages.data[0].content[0].text.value

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

load_dotenv()

def generate_audio_from_text(text):
    XI_API_KEY = os.getenv('XI_API_KEY')
    if not XI_API_KEY:
        st.error("XI_API_KEY no está definida en las variables de entorno.")
        return None

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/F2fwisJKWTUIhOEi3FuZ"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": XI_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.9,
            "similarity_boost": 0.8
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            base64_audio = base64.b64encode(response.content).decode('utf-8')
            audio_html = f'<audio controls autoplay><source src="data:audio/mpeg;base64,{base64_audio}" type="audio/mpeg"></audio>'
            return audio_html
        else:
            st.error(f"Error en la solicitud de texto a voz: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        st.error("La solicitud de audio ha excedido el tiempo de espera. Por favor, intenta de nuevo.")
        return None

# Streamlit app title
st.markdown("<h1 style='text-align: center; color: white; font-size: 24px;'>Jacobo Grinberg IA</h1>", unsafe_allow_html=True)

# Calcula el ancho de las columnas laterales para centrar la imagen
col1, col2, col3, col4, col5 = st.columns([1,2,2,2,1])

with col3:  # Utilizamos la columna central para la imagen
    st.image("img/img.jpg", width=220)  # Ajusta el ancho según sea necesario

# Agregar la descripción debajo de la imagen
st.markdown(
    """
    <p style="text-align: center;">
        Hola, soy Jacobo Grinberg, tu guía virtual en el fascinante viaje hacia el entendimiento de la conciencia y la percepción. Aquí para iluminar tus dudas sobre mis investigaciones y exploraciones en psicología y espiritualidad. Por favor, realiza tu consulta:
    </p>
    """,
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Escribe tu consulta..."):
    # Add user message to chat history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    response = get_assistant_response(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
        audio_html = generate_audio_from_text(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
