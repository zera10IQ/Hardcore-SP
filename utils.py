import json

CONFIG_FILE = "config.json"

# Función para cargar la configuración
def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # El archivo no existe: esto es normal si aún no se hace /setup
        return None
    except json.JSONDecodeError:
        # El archivo existe pero está mal escrito (falta una coma, etc.)
        print("⚠️ ERROR: El archivo 'config.json' tiene un formato inválido.")
        return None
    except Exception as e:
        # Cualquier otro error inesperado (permisos, etc.)
        print(f"❌ Error inesperado al leer config.json: {e}")
        return None
    
def load_config():
    """Carga la configuración desde el archivo JSON."""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_config(ip, port):
    """Guarda la IP y el puerto en el archivo JSON."""
    data = {"ip": ip, "port": port}
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error guardando configuración: {e}")
        return False