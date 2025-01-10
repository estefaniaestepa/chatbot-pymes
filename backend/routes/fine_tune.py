from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import openai
import os

fine_tune_bp = Blueprint('fine_tune', __name__)

# 📌 Iniciar Fine-Tuning
@fine_tune_bp.route('/start', methods=['POST'])
@jwt_required()
def start_fine_tune():
    """
    Inicia el proceso de Fine-Tuning con un archivo JSONL.
    """
    try:
        # Validar archivo
        file = request.files.get('file')
        if not file or not file.filename.endswith('.jsonl'):
            return jsonify({"error": "Se requiere un archivo JSONL válido"}), 400

        # Guardar archivo localmente
        file_path = os.path.join('data/processed', file.filename)
        if not os.path.exists('data/processed'):
            os.makedirs('data/processed')
        file.save(file_path)

        print(f"Archivo guardado en: {file_path}")

        # Subir archivo a OpenAI
        with open(file_path, 'rb') as f:
            openai_file = openai.files.create(
                file=f,
                purpose='fine-tune'
            )

        # Acceder correctamente al ID del archivo
        training_file_id = openai_file.id if hasattr(openai_file, 'id') else openai_file['id']

        print(f"Archivo subido a OpenAI, ID: {training_file_id}")

        # Iniciar Fine-Tuning
        response = openai.fine_tuning.jobs.create(
            training_file=training_file_id,
            model="gpt-4o-2024-08-06"
        )

        print(f"Fine-Tuning iniciado: {response}")

        return jsonify({
            "message": "Fine-Tuning iniciado correctamente",
            "fine_tune_id": response.id if hasattr(response, 'id') else response['id'],
            "training_file": training_file_id
        }), 200

    except openai.OpenAIError as e:
        print(f"Error de OpenAI: {e}")
        return jsonify({"error": f"Error de OpenAI: {str(e)}"}), 500
    except Exception as e:
        print(f"Error general: {e}")
        return jsonify({"error": f"Error al iniciar el Fine-Tuning: {str(e)}"}), 500
    

    
# 📌 Verificar Estado de Fine-Tuning
@fine_tune_bp.route('/status/<string:fine_tune_id>', methods=['GET'])
@jwt_required()
def fine_tune_status(fine_tune_id):
    """
    Consulta el estado de un trabajo de Fine-Tuning.
    """
    try:
        response = openai.fine_tuning.jobs.create(fine_tune_id)
        return jsonify({
            "fine_tune_id": response['id'],
            "status": response['status'],
            "created_at": response['created_at'],
            "model": response['model']
        }), 200
    except openai.OpenAIError as e:
        print(f"Error de OpenAI: {e}")
        return jsonify({"error": f"Error de OpenAI: {str(e)}"}), 500
    except Exception as e:
        print(f"Error general: {e}")
        return jsonify({"error": f"Error al verificar el estado: {str(e)}"}), 500
