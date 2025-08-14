from flask import Blueprint, request, make_response, jsonify
from ai.graph import graph
from app.database.db import save_message, init_db, get_user_conversations
import uuid
from sqlite3 import OperationalError
import time
from ai.llms import llm

bp = Blueprint('bot', __name__, url_prefix='/v1/bot')

def init_bot_blueprint():
    init_db(force_recreate=True)  # This will recreate the table with the new schema

@bp.route('/hellobot')
def hellobot():
    return "Olá, bot!"

def generate_conversation_title(message):
    prompt = f"Com base na primeira mensagem do usuário, gere um título curto e objetivo para esta conversa. Mensagem: '{message}'. Retorne apenas o título, sem explicações adicionais."
    result = llm.invoke(prompt)
    return result.content

@bp.route('/conversar', methods=['GET', 'POST', 'OPTIONS'])
def conversar():
    if request.method == 'POST':
        data = request.get_json()
        user_input = data.get("mensagem")
        thread_id = data.get("thread_id")
        user_id = data.get("user_id", "anonymous")
        title = data.get("title")  # Optional title for the conversation
        
        # Garantir que sempre temos um thread_id
        if not thread_id:
            return "O thread_id é obrigatório!", 404
        
        # Generate title if not provided
        if not title:
            title = generate_conversation_title(user_input)
        
        # Função helper para tentar salvar com retry
        def try_save_message(thread_id, user_id, message, is_bot, title, max_retries=3):
            for attempt in range(max_retries):
                try:
                    save_message(thread_id, user_id, message, is_bot=is_bot, title=title)
                    return True
                except OperationalError:
                    if attempt < max_retries - 1:
                        time.sleep(0.1 * (attempt + 1))  # Backoff exponencial
                    else:
                        raise
            return False

        # Salvar mensagens com retry
        try_save_message(thread_id, user_id, user_input, False, title)
        
        config = {"configurable": {"thread_id": thread_id}}
        ia_output = graph.invoke({"messages": user_input}, config)
        bot_response = ia_output['messages'][-1].content
        
        try_save_message(thread_id, user_id, bot_response, True, title)

        response = {
            "resposta": bot_response,
            "title": title,
            "thread_id": thread_id
        }
        return response

    return 'Página de Conversar. Envie um POST com uma mensagem!'

@bp.route('/conversas/<user_id>', methods=['GET'])
def get_conversas(user_id):
    conversations = get_user_conversations(user_id)
    return jsonify({
        "user_id": user_id,
        "conversations": conversations
    })

@bp.route('/novo-thread', methods=['GET'])
def novo_thread():
    thread_id = str(uuid.uuid4())
    return jsonify({
        "thread_id": thread_id
    })

