from flask import Blueprint, request, jsonify
from services.pdf_processor import process_pdfs
from models.document import save_document, get_all_documents, get_document_by_name, delete_document_by_name
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

# Crear Blueprint
documents_bp = Blueprint('documents', __name__)

# 📌 Ruta para subir y procesar archivos PDF
@documents_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_pdfs():
    """
    Permite subir archivos PDF y almacenarlos en la base de datos.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No se adjuntó ningún archivo"}), 400

    files = request.files.getlist('file')
    uploaded_by = get_jwt_identity()

    if not os.path.exists('data/raw_pdfs'):
        os.makedirs('data/raw_pdfs')

    processed_files = []
    for file in files:
        if file.filename.endswith('.pdf'):
            file_path = os.path.join('data/raw_pdfs', file.filename)
            file.save(file_path)
            content = process_pdfs(file_path)
            save_document(file.filename, content, uploaded_by)
            processed_files.append(file.filename)
        else:
            return jsonify({"error": f"El archivo {file.filename} no es un PDF válido"}), 400

    return jsonify({
        "message": "Archivos PDF procesados exitosamente",
        "files": processed_files
    }), 201


# 📌 Ruta para listar todos los documentos
@documents_bp.route('/all', methods=['GET'])
@jwt_required()
def list_documents():
    """
    Devuelve una lista de todos los documentos almacenados.
    """
    try:
        documents = get_all_documents()
        return jsonify({"documents": documents}), 200
    except Exception as e:
        print(f"Error en /documents/all: {str(e)}")
        return jsonify({"error": "Error interno al listar documentos"}), 500


# 📌 Ruta para obtener un documento por nombre
@documents_bp.route('/<string:filename>', methods=['GET'])
@jwt_required()
def get_document(filename):
    """
    Devuelve el contenido de un documento específico por su nombre.
    """
    try:
        document = get_document_by_name(filename)
        if document:
            return jsonify(document), 200
        return jsonify({"error": f"No se encontró el documento: {filename}"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al obtener el documento: {str(e)}"}), 500


# 📌 Ruta para eliminar un documento
@documents_bp.route('/<string:filename>', methods=['DELETE'])
@jwt_required()
def delete_document_route(filename):
    """
    Elimina un documento específico por su nombre.
    """
    try:
        result = delete_document_by_name(filename)
        if result > 0:
            return jsonify({"message": f"Documento '{filename}' eliminado exitosamente"}), 200
        return jsonify({"error": f"No se encontró el documento: {filename}"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el documento: {str(e)}"}), 500