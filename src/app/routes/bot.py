from flask import Blueprint, request, make_response, jsonify, current_app
from ai.auditing_agent.graph import graph
# from ai.evaluating_agent.graph import graph
from app.database.db import save_message, init_db, get_user_conversations, get_thread_title
import uuid
from sqlite3 import OperationalError
import time
from ai.auditing_agent.llms import llm

bp = Blueprint('bot', __name__, url_prefix='/v1/bot')

def init_bot_blueprint():
    current_app.logger.info("Inicializando banco de dados do bot")
    try:
        init_db(force_recreate=True)
        current_app.logger.info("Banco de dados do bot inicializado com sucesso")
    except Exception as e:
        current_app.logger.error(f"Erro ao inicializar banco de dados do bot: {str(e)}", exc_info=True)

@bp.route('/hellobot')
def hellobot():
    current_app.logger.debug("Rota de teste do bot acessada")
    return "Olá, bot!"

def generate_conversation_title(message):
    current_app.logger.debug(f"Gerando título para conversa a partir da mensagem: '{message[:50]}...'")
    prompt = f"Com base na primeira mensagem do usuário, gere um título curto e objetivo para esta conversa. Mensagem: '{message}'. Retorne apenas o título, sem explicações adicionais."
    result = llm.invoke(prompt)
    title = result.content
    current_app.logger.debug(f"Título gerado para conversa: '{title}'")
    return title

@bp.route('/conversar', methods=['GET', 'POST', 'OPTIONS'])
def conversar():
    if request.method == 'POST':
        current_app.logger.info("Nova requisição para conversa com o bot")
        data = request.get_json()
        user_input = data.get("mensagem")
        thread_id = data.get("thread_id")
        user_id = data.get("user_id", "anonymous")
        
        current_app.logger.debug(f"Dados da conversa - thread_id: {thread_id}, user_id: {user_id}")
        
        # Garantir que sempre temos um thread_id
        if not thread_id:
            current_app.logger.warning("Requisição sem thread_id")
            return "O thread_id é obrigatório!", 404

        # Verifique se já existe um título para o thread_id no banco
        title = get_thread_title(thread_id)
        if not title:
            current_app.logger.debug(f"Gerando título para nova thread: {thread_id}")
            title = generate_conversation_title(user_input)

        # Função helper para tentar salvar com retry
        def try_save_message(thread_id, user_id, message, is_bot, title, max_retries=3):
            for attempt in range(max_retries):
                try:
                    save_message(thread_id, user_id, message, is_bot=is_bot, title=title)
                    return True
                except OperationalError as e:
                    current_app.logger.warning(f"Tentativa {attempt+1}/{max_retries} falhou ao salvar mensagem: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(0.1 * (attempt + 1))  # Backoff exponencial
                    else:
                        current_app.logger.error(f"Falha ao salvar mensagem após {max_retries} tentativas", exc_info=True)
                        raise
            return False

        # Salvar mensagens com retry
        current_app.logger.debug("Salvando mensagem do usuário")
        try_save_message(thread_id, user_id, user_input, False, title)
        
        current_app.logger.info("Processando mensagem no modelo de linguagem")
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            ia_output = graph.invoke({"messages": user_input}, config)
            bot_response = ia_output['messages'][-1].content
            current_app.logger.debug("Resposta gerada pelo modelo de linguagem")
        except Exception as e:
            current_app.logger.error(f"Erro ao processar mensagem no modelo: {str(e)}", exc_info=True)
            bot_response = "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente."
        
        current_app.logger.debug("Salvando resposta do bot")
        try_save_message(thread_id, user_id, bot_response, True, title)

        response = {
            "resposta": bot_response,
            "title": title,
            "thread_id": thread_id
        }
        current_app.logger.info(f"Conversa processada com sucesso para thread: {thread_id}")
        return response

    return 'Página de Conversar. Envie um POST com uma mensagem!'

@bp.route('/conversas/<user_id>', methods=['GET'])
def get_conversas(user_id):
    current_app.logger.info(f"Buscando conversas para o usuário: {user_id}")
    
    try:
        conversations = get_user_conversations(user_id)
        current_app.logger.debug(f"Encontradas {len(conversations)} conversas para o usuário {user_id}")
        return jsonify({
            "user_id": user_id,
            "conversations": conversations
        })
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar conversas do usuário {user_id}: {str(e)}", exc_info=True)
        return jsonify({
            "erro": "Falha ao recuperar conversas",
            "detalhes": str(e)
        }), 500

@bp.route('/novo-thread', methods=['GET'])
def novo_thread():
    thread_id = str(uuid.uuid4())
    current_app.logger.info(f"Novo thread criado: {thread_id}")
    return jsonify({
        "thread_id": thread_id
    })

