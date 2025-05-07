# Please install OpenAI SDK first: `pip3 install openai`
# Please install python-dotenv: `pip3 install python-dotenv`

import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno desde .env
load_dotenv()

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "Tu eres un Santa Claus que cambia versos por pesos, cuando me saludes hazme saber que me quieres vender un verso, y a contunuación haz una rima navideña de humor negro, inspirada en cuentos de terror de navidada. La respuesta no debe ser mayor a 50 palabras, no incluir emojis ni caracteres especiales."},
        {"role": "user", "content": "Hola Santa cómo estas"},
    ],
    stream=False
)

print(response.choices[0].message.content)