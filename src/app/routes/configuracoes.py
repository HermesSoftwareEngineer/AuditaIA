from flask import Blueprint, request, current_app
from models.configuracoes import cadastrarPrompt, excluirPrompt, listar_prompts, atualizarPrompt
from ai.auditing_agent.prompts_loader import carregar_e_salvar_prompts

bp = Blueprint('configuracoes', __name__, url_prefix='/v1/configuracoes')

@bp.before_request
def executar_em_toda_requisicao():
    current_app.logger.debug("Carregando prompts antes da requisição")
    carregar_e_salvar_prompts()

@bp.route('prompt/incluir', methods=['POST'])
def incluir_prompt():
    if request.method == 'POST':
        current_app.logger.info("Iniciando inclusão de novo prompt")
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        prompt_text = data.get("prompt_text")
        context = data.get("context")
        tools_list = data.get("tools")

        current_app.logger.debug(f"Dados recebidos para inclusão de prompt: título='{title}', contexto='{context}'")
        response = cadastrarPrompt(title, description, prompt_text, context, tools_list)

        if not response['sucess']:
            current_app.logger.warning(f"Erro ao incluir prompt: {response['description']}")
            return {
                'Erro: ': response['description']
            }, 400
        
        current_app.logger.info(f"Prompt '{title}' incluído com sucesso")
        return {
            "Prompt Incluído": response['content']
        }, 200
    return "Método não permitido!", 405

@bp.route('/prompt/listar/', methods=['GET'])
def listar_prompts_endpoint():
    if request.method == 'GET':
        current_app.logger.info("Listando prompts cadastrados")
        prompts = listar_prompts()
        if not prompts['sucess']:
            current_app.logger.warning(f"Erro ao listar prompts: {prompts['content'].get('erro', 'Erro desconhecido')}")
            return {
                'Erro: ': prompts['content']['erro']
            }, 400
        
        current_app.logger.info(f"Retornando {len(prompts['content'])} prompts cadastrados")
        return {
            "Prompts": prompts['content']
        }, 200
    return "Método não permitido!", 405

@bp.route('/prompt/deletar/<int:id>', methods=['DELETE'])
def deletar_prompt(id):
    if request.method == 'DELETE':
        current_app.logger.info(f"Iniciando exclusão do prompt ID {id}")
        
        response = excluirPrompt(id)
        
        if not response['sucess']:
            current_app.logger.warning(f"Erro ao deletar prompt ID {id}: {response['content']}")
            return response['content'], 400

        current_app.logger.info(f"Prompt ID {id} excluído com sucesso")
        return {
            'Prompt Deletado: ': response['content']
        }, 200
    return "Método não permitido!", 405

@bp.route('/prompt/atualizar/<int:id>', methods=['PUT'])
def atualizar_prompt(id):
    if request.method == 'PUT':
        current_app.logger.info(f"Iniciando atualização do prompt ID {id}")
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        prompt_text = data.get("prompt_text")
        context = data.get("context")
        tools = data.get("tools")

        current_app.logger.debug(f"Dados para atualização do prompt ID {id}: título='{title}', contexto='{context}'")
        response = atualizarPrompt(id, title, description, prompt_text, context, tools)
        print('Response:', response)

        if not response['success']:
            current_app.logger.warning(f"Erro ao atualizar prompt ID {id}: {response['erro']}")
            return {
                'Erro: ': response['erro']
            }, 400
        
        current_app.logger.info(f"Prompt ID {id} atualizado com sucesso")
        return {
            "Prompt Atualizado": response['content']
        }, 200
    return "Método não permitido!", 405