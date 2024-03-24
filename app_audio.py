# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git remote add origin https://github.com/nicoig/ClonGPT.git
# git commit -m "Initial commit"
# git push -u origin master


# Actualizar Repo de Github
# git add .
# git commit -m "Se actualizan las variables de entorno"
# git push origin master

'''
git add .
git commit -m "Se actualizan las variables de entorno"
git push origin master
'''

# En Render
# agregar en variables de entorno
# PYTHON_VERSION = 3.9.12

################################################


import streamlit as st
import time
import os
from dotenv import load_dotenv
import openai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

st.set_page_config(
    page_title="ClonGPT",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

load_dotenv()
api_key = os.getenv("OPENAI_APIKEY")
assistant_id = os.getenv("ASSISTANT_ID")

@st.cache_resource
def load_openai_client_and_assistant():
    client = openai.OpenAI(api_key=api_key)
    my_assistant = client.beta.assistants.retrieve(assistant_id)
    thread = client.beta.threads.create()
    return client, my_assistant, thread

client, my_assistant, assistant_thread = load_openai_client_and_assistant()

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(0.5)
    return run

def get_assistant_response(user_input=""):
    with st.spinner('Escribiendo Respuesta...'):
        message = client.beta.threads.messages.create(thread_id=assistant_thread.id, role="user", content=user_input)
        run = client.beta.threads.runs.create(thread_id=assistant_thread.id, assistant_id=assistant_id)
        run = wait_on_run(run, assistant_thread)
        messages = client.beta.threads.messages.list(thread_id=assistant_thread.id, order="asc", after=message.id)
        return messages.data[0].content[0].text.value

def save_conversation_to_pdf(conversation):
    c = canvas.Canvas("conversation.pdf", pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    for line in conversation:
        c.drawString(10, height - 10, line)
        height -= 15
    c.save()

st.markdown("<h1 style='text-align: center; color: white; font-size: 24px;'>ClonGPT</h1>", unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1,1,1,1,2,1,1,1,1])

with col5:
    st.image("img/img.jpg", width=240)

st.markdown(""" <p style="text-align: center;"> Hola, soy ClonGPT, un asistente virtual creado para responder sobre cualquier tema que desees. Puedes cargarme archivos y realizar consultas sobre ellos, o simplemente hacer preguntas sobre cualquier asunto que te interese. Estoy aquí para ayudarte de la mejor manera posible. </p> """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu consulta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response = get_assistant_response(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})