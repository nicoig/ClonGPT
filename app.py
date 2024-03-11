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

# Set your OpenAI API key and assistant ID here
api_key = st.secrets["openai_apikey"]
assistant_id = st.secrets["assistant_id"]

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

# Streamlit app title
st.markdown("<h1 style='text-align: center; color: white; font-size: 24px;'>JacoBOT Grinberg</h1>", unsafe_allow_html=True)

# Calcula el ancho de las columnas laterales para centrar la imagen
col1, col2, col3 = st.columns([1,2,1])

with col2:  # Usamos la columna central para la imagen
    st.image("img/img.jpg", width=2200)  # Ajusta el ancho según sea necesario


# Agregar la descripción debajo de la imagen
st.markdown(
    """
    <p style="text-align: center;">
        Hola, soy JacoBOT Grinberg, tu guía virtual en el fascinante viaje hacia el entendimiento de la conciencia y la percepción. Aquí para iluminar tus dudas sobre mis investigaciones y exploraciones en psicología y espiritualidad.
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

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
