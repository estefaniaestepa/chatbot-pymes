import openai
from config.openai import openai

def chat_with_model(user_message):
    """
    Envía un mensaje al modelo fine-tuneado de OpenAI y devuelve la respuesta.
    """
    try:
        response = openai.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:upgrade-hub::AggAyOUR",
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=9000,
            temperature=0.6,
            top_p=1.0
        )
        
        # Extraer la respuesta correctamente
        bot_response = response.choices[0].message.content if response.choices else "No se recibió respuesta del modelo."
        return bot_response
    
    except openai.OpenAIError as e:
        raise Exception(f"Error al interactuar con OpenAI: {e}")