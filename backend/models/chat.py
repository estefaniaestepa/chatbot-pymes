from config.db import db
from datetime import datetime

# Referencia a la colección de chats
chats_collection = db.get_collection("chats")

def create_chat_entry(user_message, bot_response, user_id=None):
    """
    Guarda un nuevo mensaje de chat en la base de datos.
    """
    chat_entry = {
        "user_id": user_id,
        "user_message": user_message,
        "bot_response": bot_response,
        "timestamp": datetime.utcnow()
    }
    result = chats_collection.insert_one(chat_entry)
    return result.inserted_id

def get_user_chats(user_id):
    """
    Recupera todos los chats de un usuario específico.
    """
    chats = chats_collection.find({"user_id": user_id})
    return list(chats)

def get_all_chats():
    """
    Recupera todos los chats almacenados.
    """
    chats = chats_collection.find()
    return list(chats)