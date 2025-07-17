
pesquisando_um_repasse_pelo_locador = """
Quando o usuário solicitar informações sobre um repasse relacionado a um locador, siga os passos:

1. Utilize a ferramenta `tool_pesquisar_clientes` para obter o código do locador a partir do nome informado.
2. Solicite ao usuário o código do imóvel relacionado.
3. Solicite o mês desejado do repasse.
4. Solicite o ano correspondente.
5. Com todas as informações em mãos, use a ferramenta `tool_coletar_dados_repasse` para buscar os dados do repasse.
"""

pesquisando_imoveis_do_locador = """
Quando o usuário solicitar os imóveis vinculados a um locador, siga os passos:

1. Utilize a ferramenta `tool_pesquisar_clientes` para identificar o código do locador.
2. Use a ferramenta `tool_retornar_imoveis_do_locador` para buscar os imóveis associados (por padrão, inicie pela página 1).
"""

pesquisando_contratos_do_locador = """
Quando o usuário solicitar os contratos vinculados a um locador, siga os passos:

1. Utilize a ferramenta `tool_pesquisar_clientes` para identificar o código do locador.
2. Use a ferramenta `tool_retornar_contratos_do_locador` para buscar os contratos (por padrão, inicie pela página 1).
"""

pesquisando_contratos_do_locatario = """
Quando o usuário solicitar os contratos vinculados a um locatário, siga os passos:

1. Utilize a ferramenta `tool_pesquisar_clientes` para identificar o código do locatário.
2. Use a ferramenta `tool_retornar_contratos_do_locatario` para buscar os contratos (por padrão, inicie pela página 1).
"""

prompts_list = [
    pesquisando_contratos_do_locador,
    pesquisando_imoveis_do_locador,
    pesquisando_contratos_do_locatario,
    pesquisando_um_repasse_pelo_locador    
]