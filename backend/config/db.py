from pymongo import MongoClient
from config.settings import Config

try:
    # Crear conexión con MongoDB
    client = MongoClient(Config.MONGO_URI)
    db = client.get_database()
    print("✅ Conexión a MongoDB exitosa.")
except Exception as e:
    print(f"❌ Error al conectar con MongoDB: {e}")
    db = None