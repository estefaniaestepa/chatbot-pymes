import openai
from config.settings import Config

# Configurar clave de API de OpenAI
try:
    openai.api_key = Config.OPENAI_API_KEY
    print("✅ Clave de API de OpenAI configurada correctamente.")
except Exception as e:
    print(f"❌ Error al configurar la clave de API de OpenAI: {e}")