from flask import Blueprint, request, jsonify
from models.user import create_user, get_user_by_email
import bcrypt
from flask_jwt_extended import create_access_token
from config.settings import Config

# Crear Blueprint para autenticación
auth_bp = Blueprint('auth', __name__)

# 📌 Ruta para registrar un usuario
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registra un nuevo usuario.
    """
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "El correo ya está registrado"}), 400

    # Cifrar contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Crear usuario
    user_id = create_user(username, email, hashed_password.decode('utf-8'))
    return jsonify({
        "message": "Usuario registrado exitosamente",
        "user_id": str(user_id)
    }), 201


# 📌 Ruta para iniciar sesión
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Inicia sesión y devuelve un token JWT.
    """
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Correo y contraseña son obligatorios"}), 400

    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Verificar contraseña
    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return jsonify({"error": "Contraseña incorrecta"}), 401

    # Generar token JWT con claim 'sub'
    access_token = create_access_token(
        identity=str(user['_id']),  # El claim 'sub' se configura automáticamente
        additional_claims={"username": user['username']}
    )

    return jsonify({
        "message": "Inicio de sesión exitoso",
        "token": access_token
    }), 200