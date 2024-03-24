# ClonGPT

ClonGPT es una aplicación de asistente virtual creada con Streamlit y OpenAI. Esta aplicación te permite tener una conversación interactiva con un asistente virtual, similar a ChatGPT, pero personalizado con tus propias preferencias.

## Características principales

- **Interfaz de chat intuitiva**: La aplicación presenta una interfaz de chat limpia y fácil de usar, donde puedes escribir tus consultas y recibir respuestas del asistente virtual.
- **Integración con OpenAI**: ClonGPT utiliza la API de OpenAI para generar respuestas inteligentes y relevantes a tus preguntas.
- **Personalización del asistente**: Puedes configurar y personalizar el comportamiento del asistente virtual, ajustando sus parámetros y preferencias según tus necesidades.
- **Generación de PDF**: La aplicación te permite guardar las conversaciones completas en un archivo PDF para futuras referencias.

## Requisitos

- Python 3.x
- Streamlit
- OpenAI
- ReportLab

## Instalación

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias ejecutando `pip install -r requirements.txt`.
3. Configura tus credenciales de OpenAI creando un archivo `.env` en la raíz del proyecto y agregando tus claves de API de OpenAI:

OPENAI_APIKEY=tu_clave_api
ASSISTANT_ID=id_de_tu_asistente

## Uso

1. Ejecuta la aplicación con `streamlit run app.py`.
2. La aplicación se abrirá en tu navegador web predeterminado.
3. Escribe tus consultas en el campo de entrada y el asistente virtual generará respuestas relevantes.
4. Puedes guardar la conversación completa en un archivo PDF haciendo clic en el botón correspondiente.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar esta aplicación, por favor, crea un issue o envía una solicitud de extracción.

## Licencia

Este proyecto está bajo la Licencia MIT. 

