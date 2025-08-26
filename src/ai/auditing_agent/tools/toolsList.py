from .clienteTools import tool_pesquisar_clientes
from .contratosTools import tool_retornar_contratos_do_locador, tool_retornar_contratos_do_locatario
from .imoveisTools import tool_retornar_imoveis_do_locador, tool_retornar_imoveis_disponiveis
from .extratosTools import tool_coletar_dados_repasse, tool_coletar_dados_extrato_locatario
from .movimentosTools import tool_retornar_movimentos
from .webSearchTools import web_search_properties, browse_page_content
from .propertyValuation import avaliar_imovel

toolsList = [
    tool_coletar_dados_repasse,
    tool_pesquisar_clientes,
    tool_retornar_imoveis_do_locador,
    tool_retornar_contratos_do_locador,
    tool_retornar_contratos_do_locatario,
    tool_retornar_movimentos,
    tool_retornar_imoveis_disponiveis,
    tool_coletar_dados_extrato_locatario,
    web_search_properties,
    avaliar_imovel
    # browse_page_content
]