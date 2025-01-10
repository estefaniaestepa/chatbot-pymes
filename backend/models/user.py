from config.db import db
from datetime import datetime
from bson.objectid import ObjectId

# Referencia a la colección de usuarios
users_collection = db.get_collection("users")

def create_user(username, email, password_hash):
    """
    Crea un nuevo usuario en la base de datos.
    """
    user_entry = {
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = users_collection.insert_one(user_entry)
    return result.inserted_id

def get_user_by_email(email):
    """
    Recupera un usuario por su correo electrónico.
    """
    return users_collection.find_one({"email": email})

def get_user_by_id(user_id):
    """
    Recupera un usuario por su ID.
    """
    return users_collection.find_one({"_id": ObjectId(user_id)})

def update_user(user_id, updates: dict):
    """
    Actualiza la información de un usuario.
    """
    updates["updated_at"] = datetime.utcnow()
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updates}
    )
    return result.modified_count

def delete_user(user_id):
    """
    Elimina un usuario por su ID.
    """
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count