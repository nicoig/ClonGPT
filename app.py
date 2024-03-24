# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git remote add origin https://github.com/nicoig/GPT-Clone.git
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
from openai import OpenAI
import os
from dotenv import load_dotenv
from openai.file_upload import FileUpload

# Carga las variables de entorno desde el archivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
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
def get_assistant_response(user_input="", file_id=None):
    with st.spinner('Escribiendo Respuesta...'):
        message = client.beta.threads.messages.create(thread_id=assistant_thread.id, role="user", content=user_input, file_ids=[file_id] if file_id else [])
        run = client.beta.threads.runs.create(thread_id=assistant_thread.id, assistant_id=assistant_id)
        run = wait_on_run(run, assistant_thread)
        messages = client.beta.threads.messages.list(thread_id=assistant_thread.id, order="asc", after=message.id)
        return messages.data[0].content[0].text.value

# Function to upload a file and get its ID
def upload_file(file_path):
    openai = OpenAI(api_key=api_key)
    file_upload = FileUpload(openai, file_path, purpose="assistants")
    file_id = file_upload.upload()
    return file_id

# Streamlit app title
st.markdown("<h1 style='text-align: center; color: white; font-size: 24px;'>ClonGPT</h1>", unsafe_allow_html=True)

# Utiliza 7 columnas para un centrado más preciso
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1,1,1,1,2,1,1,1,1])

with col5: # Esta es la columna central
    st.image("img/img.jpg", width=240) # Ajusta el ancho de la imagen según sea necesario

# Agregar la descripción debajo de la imagen
st.markdown("""
<p style="text-align: center;">
Hola, soy ClonGPT, un asistente virtual creado para responder sobre cualquier tema que desees. Puedes cargarme archivos y realizar consultas sobre ellos, o simplemente hacer preguntas sobre cualquier asunto que te interese. Estoy aquí para ayudarte de la mejor manera posible.
</p>
""", unsafe_allow_html=True)

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

    # Allow user to upload a file
    file_upload = st.file_uploader("Carga un archivo", type=["pdf", "txt", "docx"])
    if file_upload is not None:
        file_path = f"temp/{file_upload.name}"
        with open(file_path, "wb") as f:
            f.write(file_upload.getbuffer())
        file_id = upload_file(file_path)
        os.remove(file_path)

        # Get assistant response with file
        response = get_assistant_response(prompt, file_id=file_id)
    else:
        # Get assistant response without file
        response = get_assistant_response(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})