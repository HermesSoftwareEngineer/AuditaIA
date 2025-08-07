from flask import Blueprint, request, make_response
from ai.graph import graph

bp = Blueprint('bot', __name__, url_prefix='/v1/bot')

@bp.route('/hellobot')
def hellobot():
    return "Olá, bot!"

@bp.route('/conversar', methods=['GET', 'POST', 'OPTIONS'])
def conversar():
    if request.method == 'POST':
        data = request.get_json()
        user_input = data.get("mensagem")
        thread_id = data.get("thread_id")
        config = {"configurable": {"thread_id": thread_id}}
        ia_output = graph.invoke({"messages": user_input}, config)

        response = {
            "resposta": ia_output['messages'][-1].content
        }
        return response
    return 'Página de Conversar. Envie um POST com uma mensagem!'

