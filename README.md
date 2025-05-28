# objeto-parlante

Un asistente con voz que puede escuchar tus preguntas y responder con audio.

## Requisitos

### Variables de entorno
Necesita un archivo con las variables de entorno:
 
```
#.env
ELEVENLABS_API_KEY=  # Para conversión de texto a voz
DEEPSEEK_API_KEY=    # Para generación de texto
OPENAI_API_KEY=      # Para transcripción de audio a texto
```

### Dependencias

Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Uso

### Usando texto escrito
```bash
python main.py --texto "Hola Santa cómo estas"
```

### Usando el micrófono
```bash
python main.py --duracion 5  # Graba durante 5 segundos
```

### Opciones adicionales
```bash
python main.py --no-audio  # No reproduce la respuesta como audio
```
