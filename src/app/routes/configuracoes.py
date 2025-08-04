from flask import Blueprint, request, jsonify
from controllers.bot import cadastrarPrompt

bp = Blueprint('configuracoes', __name__, url_prefix='/v1/configuracoes')

@bp.route('incluirPrompt', methods=['GET', 'POST'])
def incluir_prompt():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        prompt_text = data.get("prompt_text")
        context = data.get("context")
        tools_list = data.get("tools")

        response = cadastrarPrompt(title, description, prompt_text, context, tools_list)

        if not response['sucess']:
            return {
                'Erro: ': response['description']
            }, 400
        
        return {
            "Prompt Incluído": response['content']
        }, 200
    return "Página de cadastro de prompt. Envie um prompt com os dados de ...!"