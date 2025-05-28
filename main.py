# Please install OpenAI SDK first: `pip3 install openai`
# Please install python-dotenv: `pip3 install python-dotenv`
# Please install: `pip3 install sounddevice soundfile numpy`

import os
import time
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from textoavoz import text_to_speech_file, play
from vozatexto import grabar_y_transcribir

# Cargar variables de entorno desde .env
load_dotenv()

def procesar_texto(texto_entrada):
    """
    Procesa el texto de entrada usando la API de OpenAI y devuelve la respuesta.
    
    Args:
        texto_entrada (str): Texto de entrada para el asistente.
        
    Returns:
        str: Respuesta generada por el asistente.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu eres un Santa Claus que cambia versos por pesos, cuando me saludes hazme saber que me quieres vender un verso, y a contunuación haz una rima navideña de humor negro, inspirada en cuentos de terror de navidada. La respuesta no debe ser mayor a 50 palabras, no incluir emojis ni caracteres especiales."},
            {"role": "user", "content": texto_entrada},
        ],
        stream=False
    )
    
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description='Objeto Parlante - Un asistente con voz')
    parser.add_argument('--texto', '-t', help='Texto de entrada (si no se proporciona, se grabará audio)')
    parser.add_argument('--duracion', '-d', type=int, default=5, help='Duración de la grabación en segundos (por defecto 5)')
    parser.add_argument('--no-audio', action='store_true', help='No reproducir la respuesta como audio')
    
    args = parser.parse_args()
    
    try:
        # Si no se proporciona texto, grabar audio y transcribirlo
        if args.texto:
            texto_entrada = args.texto
            print(f"Texto proporcionado: {texto_entrada}")
        else:
            print(f"Preparado para grabar. Habla cuando veas 'Grabando...'")
            print(f"\n3...")
            time.sleep(1)
            print(f"2...")
            time.sleep(1)
            print(f"1...")
            time.sleep(1)
            print(f"\n¡Grabando durante {args.duracion} segundos!")
            
            texto_entrada = grabar_y_transcribir(duracion=args.duracion)
            
            if not texto_entrada:
                print("No se pudo transcribir el audio. Inténtalo de nuevo o proporciona texto con --texto.")
                return
                
            print(f"\nTexto transcrito: '{texto_entrada}'")
        
        # Procesar el texto con OpenAI
        print("\nProcesando con OpenAI...")
        respuesta = procesar_texto(texto_entrada)
        print("\nRespuesta del asistente:")
        print(respuesta)
        
        # Convertir la respuesta a voz y reproducirla
        if not args.no_audio:
            print("\nConvirtiendo respuesta a voz...")
            archivo_audio = text_to_speech_file(respuesta)
            
            # Reproducir el audio
            with open(archivo_audio, "rb") as f:
                audio_data = f.read()
                print("Reproduciendo audio...")
                play(audio_data)
    
    except Exception as e:
        print(f"\nError: {e}")
        print("Verifica que tienes las claves de API de OpenAI y ElevenLabs correctas en el archivo .env y que los paquetes necesarios están instalados.")
        print("Puedes ejecutar: pip install -r requirements.txt")
        
        # Sugerencias de solución de problemas
        if "api_key" in str(e).lower():
            print("\nProblema con la clave de API. Verifica tus claves en el archivo .env")
        elif "sound" in str(e).lower() or "audio" in str(e).lower():
            print("\nProblema con el dispositivo de audio. Verifica que tu micrófono esté conectado y funcionando.")
        
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()