import openai

def start_fine_tune(file_path):
    """
    Inicia el proceso de fine-tuning con un archivo JSONL.
    """
    response = openai.fine_tuning.jobs.create(training_file=file_path, model="gpt-4o")
    return response['id']


def get_fine_tune_status(fine_tune_id):
    """
    Devuelve el estado del proceso de fine-tuning.
    """
    response = openai.fine_tuning.jobs.retrieve(id=fine_tune_id)
    return response['status']