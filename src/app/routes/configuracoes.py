from flask import Blueprint, request
from models.configuracoes import cadastrarPrompt, excluirPrompt, listar_prompts

bp = Blueprint('configuracoes', __name__, url_prefix='/v1/configuracoes')

@bp.route('prompt', methods=['GET', 'POST'])
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
    elif request.method == 'GET':
        prompts = listar_prompts()
        if not prompts['sucess']:
            return {
                'Erro: ': prompts['content']['erro']
            }, 400
        
        return {
            "Prompts": prompts['content']
        }, 200
    return "Página de cadastro de prompt. Envie um prompt com os dados de ...!"

@bp.route('/prompt/<int:id>', methods=['GET','DELETE'])
def deletar_prompt(id):
    if request.method == 'DELETE':
        
        response = excluirPrompt(id)
        
        if not response['sucess']:
            return response['content'], 400

        return {
            'Prompt Deletado: ': response['content']
        }, 200
    return "Método não permitido!", 405