from flask import Blueprint, request, jsonify
from services.chat import chat_with_model
from models.chat import create_chat_entry, get_user_chats
from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear Blueprint para Chat
chat_bp = Blueprint('chat', __name__)

# 📌 Ruta para enviar mensajes al chatbot
@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def chat():
    """
    Recibe un mensaje del usuario y devuelve una respuesta del chatbot.
    """
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "El mensaje es obligatorio"}), 400

    try:
        # Obtener el ID del usuario desde el token JWT
        user_id = get_jwt_identity()
        
        # Generar respuesta del chatbot
        bot_response = chat_with_model(user_message)
        
        # Guardar historial del chat
        chat_id = create_chat_entry(user_message, bot_response, user_id)

        return jsonify({
            "message_id": str(chat_id),
            "user_message": user_message,
            "bot_response": bot_response
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error al procesar el chat: {str(e)}"}), 500


# 📌 Ruta para obtener el historial de chats de un usuario
@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def chat_history():
    """
    Devuelve el historial de chats del usuario autenticado.
    """
    try:
        # Obtener el ID del usuario desde el token JWT
        user_id = get_jwt_identity()
        
        # Obtener el historial de chats
        chats = get_user_chats(user_id)
        
        formatted_chats = [
            {
                "user_message": chat.get('user_message'),
                "bot_response": chat.get('bot_response'),
                "timestamp": chat.get('timestamp').isoformat()
            }
            for chat in chats
        ]

        return jsonify({"history": formatted_chats}), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener el historial: {str(e)}"}), 500