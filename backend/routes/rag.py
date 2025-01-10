from flask import Blueprint, request, jsonify
from services.rag import rag_pipeline
from flask_jwt_extended import jwt_required

# Crear Blueprint para RAG
rag_bp = Blueprint('rag', __name__)

# Ruta para realizar una consulta RAG
@rag_bp.route('/query', methods=['POST'])
@jwt_required()
def query():
    """
    Realiza una consulta utilizando Retrieval-Augmented Generation (RAG).
    """
    data = request.json
    user_query = data.get('query')

    if not user_query:
        return jsonify({"error": "El parámetro 'query' es obligatorio"}), 400

    try:
        response = rag_pipeline(user_query)
        return jsonify({
            "response": response['response'],
            "source": response['source'],
            "score": response['score']
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error en el pipeline RAG: {str(e)}"}), 500

# Ruta para probar la carga de documentos RAG
@rag_bp.route('/reload', methods=['POST'])
@jwt_required()
def reload_documents():
    """
    Recarga los documentos en el sistema RAG.
    """
    from services.rag import load_documents
    try:
        load_documents()
        return jsonify({"message": "Documentos RAG recargados correctamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al recargar documentos: {str(e)}"}), 500