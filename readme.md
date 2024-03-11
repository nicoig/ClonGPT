# Jacobo Grinberg IA

Este proyecto es una aplicación interactiva de Streamlit que simula conversaciones con Jacobo Grinberg, ofreciendo respuestas generadas por IA a preguntas sobre psicología, espiritualidad y las investigaciones de Grinberg. Utiliza la API de OpenAI para generar las respuestas y la API de ElevenLabs para convertir el texto de las respuestas en audio.

## Características

- Interfaz de chat para interactuar con la IA que simula a Jacobo Grinberg.
- Respuestas en texto generadas por la API de OpenAI.
- Conversión de respuestas de texto a audio mediante la API de ElevenLabs.

## Cómo usar

Para utilizar la aplicación, simplemente ingresa tu consulta en el campo de texto disponible y la IA responderá. También puedes escuchar la respuesta en formato de audio.

## Instalación

Para ejecutar esta aplicación en tu entorno local, sigue estos pasos:

1. Clona este repositorio:

git clone https://github.com/nicoig/jacobo-grinberg-ia


2. Instala las dependencias:

pip install -r requirements.txt


3. Ejecuta la aplicación de Streamlit:

streamlit run app_audio.py


## Configuración

Para configurar las claves API necesarias para OpenAI y ElevenLabs, sigue estos pasos:

1. Crea un archivo `.env` en el directorio raíz del proyecto con el siguiente contenido, reemplazando `<tu-clave-api>` con tus respectivas claves API:

OPENAI_APIKEY=<tu-clave-api-de-openai>
ASSISTANT_ID=<tu-id-de-asistente-de-openai>
XI_API_KEY=<tu-clave-api-de-elevenlabs>


2. Asegúrate de que el archivo `.env` esté listado en tu `.gitignore` para prevenir que se suba a repositorios públicos.

## Contribuir

Si te gustaría contribuir a este proyecto, por favor, crea un fork del repositorio, realiza tus cambios y envía un pull request para su revisión.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Si tienes preguntas o comentarios sobre este proyecto, por favor, no dudes en contactarme.
Recuerda reemplazar <URL-del-repositorio>, <tu-clave-api-de-openai>, <tu-id-de-asistente-de-openai>, y <tu-clave-api-de-elevenlabs> con la información correspondiente a tu proyecto. Asegúrate también de ajustar cualquier otra información específica de tu proyecto como la descripción, cómo usar, configuración y contacto.