from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.settings import Config
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.documents import documents_bp
from routes.fine_tune import fine_tune_bp
from routes.rag import rag_bp


# Inicializar la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializar JWT
jwt = JWTManager(app)

# Registrar Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(documents_bp, url_prefix='/documents')
app.register_blueprint(fine_tune_bp, url_prefix='/fine-tune')
app.register_blueprint(rag_bp, url_prefix='/rag')

# Ruta principal


@app.route('/')
def home():
    return jsonify({"message": "🚀 Backend Flask en funcionamiento correctamente."})

# Manejador de errores global


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500


# Punto de entrada principal
if __name__ == '__main__':
    app.run(host=Config.SERVER_HOST, port=Config.SERVER_PORT, debug=Config.DEBUG)
