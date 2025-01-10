import os
import json
from PyPDF2 import PdfReader

def process_pdfs(pdf_path):
    """
    Procesa un archivo PDF y extrae su contenido.
    :param pdf_path: Ruta del archivo PDF.
    :return: Contenido extraído como texto.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo PDF no existe en la ruta: {pdf_path}")

    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        return text.strip()
    except Exception as e:
        raise Exception(f"Error al procesar el PDF: {e}")


def process_pdf_folder(pdf_folder, output_file):
    """
    Procesa todos los archivos PDF en una carpeta y los guarda en un archivo JSONL.
    :param pdf_folder: Carpeta que contiene archivos PDF.
    :param output_file: Ruta del archivo JSONL resultante.
    """
    if not os.path.exists(pdf_folder):
        raise FileNotFoundError(f"La carpeta no existe: {pdf_folder}")
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    if not pdf_files:
        raise FileNotFoundError("No se encontraron archivos PDF en la carpeta proporcionada.")
    
    processed_data = []
    try:
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_folder, pdf_file)
            content = process_pdfs(pdf_path)
            processed_data.append({
                "file_name": pdf_file,
                "content": content
            })

        # Guardar el contenido en formato JSONL
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in processed_data:
                f.write(json.dumps(entry) + '\n')
    except Exception as e:
        raise Exception(f"Error al procesar la carpeta de PDFs: {e}")