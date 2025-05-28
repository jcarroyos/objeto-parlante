import os
import time
import uuid
import glob
import datetime
import sounddevice as sd
import soundfile as sf
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar cliente de OpenAI para usar Whisper
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Asegurar que existen los directorios para los archivos de audio
MENSAJES_DIR = os.path.join("audio", "mensajes")
RESPUESTAS_DIR = os.path.join("audio", "respuestas")
os.makedirs(MENSAJES_DIR, exist_ok=True)
os.makedirs(RESPUESTAS_DIR, exist_ok=True)

def grabar_audio(duracion=5, fs=44100):
    """
    Graba audio del micrófono durante el tiempo especificado.
    
    Args:
        duracion (int): Duración en segundos para grabar. Por defecto 5 segundos.
        fs (int): Frecuencia de muestreo. Por defecto 44100 Hz.
        
    Returns:
        str: Ruta del archivo de audio grabado en formato WAV.
    """
    print(f"Grabando audio durante {duracion} segundos...")
    
    # Grabar audio
    grabacion = sd.rec(int(duracion * fs), samplerate=fs, channels=1, dtype='float32')
    
    # Esperar hasta que la grabación termine
    sd.wait()
    
    print("Grabación finalizada.")
    
    # Generar un timestamp para el nombre del archivo
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uuid.uuid4()}.wav"
    
    # Ruta completa al archivo en la carpeta de mensajes
    save_file_path = os.path.join(MENSAJES_DIR, filename)
    
    # Guardar la grabación como archivo WAV
    sf.write(save_file_path, grabacion, fs)
    
    print(f"{save_file_path}: ¡El archivo de audio se guardó exitosamente!")
    return save_file_path

def transcribir_audio(archivo_audio):
    """
    Transcribe un archivo de audio a texto usando OpenAI Whisper.
    
    Args:
        archivo_audio (str): Ruta al archivo de audio a transcribir.
        
    Returns:
        str: Texto transcrito del audio.
    """
    print(f"Transcribiendo audio: {archivo_audio}")
    
    try:
        with open(archivo_audio, "rb") as audio_file:
            # Utilizar OpenAI Whisper para transcribir el audio
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            
            texto_transcrito = transcript.text
            print(f"Transcripción: {texto_transcrito}")
            return texto_transcrito
    except Exception as e:
        print(f"Error al transcribir el audio: {e}")
        return ""

def limpiar_archivos_audio(max_files=10):
    """
    Limpia archivos de audio antiguos de los directorios de mensajes y respuestas,
    dejando solo los más recientes.
    
    Args:
        max_files (int): Número máximo de archivos de audio a mantener por carpeta.
    """
    try:
        # Limpiar carpeta de mensajes
        limpiar_carpeta(MENSAJES_DIR, "*.wav", max_files)
        
        # Limpiar carpeta de respuestas
        limpiar_carpeta(RESPUESTAS_DIR, "*.mp3", max_files)
    except Exception as e:
        print(f"Error al limpiar archivos de audio: {e}")

def limpiar_carpeta(directorio, patron, max_files):
    """
    Limpia archivos que coinciden con el patrón en el directorio especificado,
    dejando solo los más recientes.
    
    Args:
        directorio (str): Ruta al directorio a limpiar.
        patron (str): Patrón glob para filtrar archivos.
        max_files (int): Número máximo de archivos a mantener.
    """
    # Asegurar que el directorio existe
    if not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)
        return
        
    # Buscar todos los archivos que coinciden con el patrón
    ruta_busqueda = os.path.join(directorio, patron)
    archivos = glob.glob(ruta_busqueda)
    
    # Si hay más archivos que el límite, eliminar los más antiguos
    if len(archivos) > max_files:
        # Ordenar por fecha de modificación (más antiguos primero)
        archivos_ordenados = sorted(archivos, key=os.path.getmtime)
        
        # Eliminar los archivos más antiguos
        for archivo in archivos_ordenados[:-max_files]:
            try:
                os.remove(archivo)
                print(f"Archivo eliminado: {archivo}")
            except Exception as e:
                print(f"No se pudo eliminar {archivo}: {e}")

# Función principal que combina grabación y transcripción
def grabar_y_transcribir(duracion=5):
    """
    Graba audio del micrófono y lo transcribe a texto.
    
    Args:
        duracion (int): Duración en segundos para grabar. Por defecto 5 segundos.
        
    Returns:
        str: Texto transcrito del audio grabado.
    """
    # Limpiar archivos de audio antiguos
    limpiar_archivos_audio()
    
    # Grabar audio
    archivo_audio = grabar_audio(duracion=duracion)
    
    # Transcribir audio
    texto = transcribir_audio(archivo_audio)
    
    return texto

# Ejemplo de uso
if __name__ == "__main__":
    # Limpiar archivos de audio antiguos, manteniendo solo los 10 más recientes
    limpiar_archivos_audio(max_files=10)
    
    # Grabar audio durante 5 segundos y transcribirlo
    texto_transcrito = grabar_y_transcribir(5)
    print(f"Texto transcrito: {texto_transcrito}")
