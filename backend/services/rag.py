import openai
from config.openai import openai
from models.document import get_all_documents
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Almacenamiento de embeddings temporales
vectorizer = TfidfVectorizer()
document_texts = []
document_metadata = []

def load_documents():
    """
    Carga todos los documentos desde MongoDB y los prepara para RAG.
    """
    global document_texts, document_metadata
    documents = get_all_documents()
    
    document_texts = [doc['content'] for doc in documents]
    document_metadata = [{"file_name": doc['file_name']} for doc in documents]
    
    if not document_texts:
        raise Exception("No hay documentos disponibles para RAG.")
    
    # Vectorizar documentos
    return vectorizer.fit_transform(document_texts)

def retrieve_relevant_document(user_query):
    """
    Recupera el documento más relevante basado en una consulta del usuario.
    :param user_query: Consulta del usuario.
    :return: Documento más relevante.
    """
    if not document_texts:
        load_documents()
    
    query_vector = vectorizer.transform([user_query])
    similarities = cosine_similarity(query_vector, vectorizer.transform(document_texts))
    
    most_relevant_index = similarities.argmax()
    most_relevant_document = document_metadata[most_relevant_index]
    most_relevant_content = document_texts[most_relevant_index]
    
    return {
        "file_name": most_relevant_document['file_name'],
        "content": most_relevant_content,
        "score": similarities[0][most_relevant_index]
    }

def rag_pipeline(user_query):
    """
    Integra la recuperación y generación para responder preguntas.
    :param user_query: Consulta del usuario.
    :return: Respuesta generada.
    """
    try:
        relevant_doc = retrieve_relevant_document(user_query)
        prompt = f"""
        Usa la siguiente información para responder la pregunta del usuario:

        Información del documento:
        {relevant_doc['content']}

        Pregunta del usuario:
        {user_query}
        """
        response = openai.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:upgrade-hub::AggAyOUR",
            messages=[
                {"role": "system", "content": "Eres un asistente experto que utiliza documentos externos para responder preguntas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.5,
            top_p=1.0
        )
        return {
            "response": response['choices'][0]['message']['content'],
            "source": relevant_doc['file_name'],
            "score": relevant_doc['score']
        }
    except Exception as e:
        raise Exception(f"Error en el pipeline RAG: {e}")