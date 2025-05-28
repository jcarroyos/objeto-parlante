import os
import time
import uuid
import glob
import sounddevice as sd
import soundfile as sf
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar cliente de OpenAI para usar Whisper
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    
    # Generar un nombre de archivo único
    save_file_path = f"{uuid.uuid4()}.wav"
    
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
    Limpia archivos de audio antiguos del directorio de trabajo,
    dejando solo los más recientes.
    
    Args:
        max_files (int): Número máximo de archivos de audio a mantener.
    """
    try:
        # Buscar todos los archivos .wav y .mp3
        archivos_audio = glob.glob("*.wav") + glob.glob("*.mp3")
        
        # Si hay más archivos que el límite, eliminar los más antiguos
        if len(archivos_audio) > max_files:
            # Ordenar por fecha de modificación (más antiguos primero)
            archivos_ordenados = sorted(archivos_audio, key=os.path.getmtime)
            
            # Eliminar los archivos más antiguos
            for archivo in archivos_ordenados[:-max_files]:
                try:
                    os.remove(archivo)
                    print(f"Archivo eliminado: {archivo}")
                except Exception as e:
                    print(f"No se pudo eliminar {archivo}: {e}")
    except Exception as e:
        print(f"Error al limpiar archivos de audio: {e}")

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
