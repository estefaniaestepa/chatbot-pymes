import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    # Configuraciones de la aplicación Flask
    DEBUG = os.getenv("DEBUG", "True") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    
    # Configuraciones de MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/proyecto-ai")
    
    # Configuraciones de OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Otras configuraciones globales
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 5000))