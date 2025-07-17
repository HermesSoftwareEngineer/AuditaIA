
pesquisando_um_repasse_pelo_locador = """
    Quando o usuário pedir pra verificar um repasse pelo nome do locador
    1 - Identifique o código do locador pela ferramenta tool_pesquisar_clientes
    2 - Peça o código do imóvel ao usuário
    3 - Peça o mês do repasse ao usuário
    4 - Peça o ano do repasse ao usuário
    5 - Pesquise o repasse usando a ferramenta tool_coletar_dados_repasse
"""

pesquisando_imoveis_do_locador = """
    Quando o usuário pedir os imóveis de um locador
    1 - Identifique o código do locador pela ferramenta tool_pesquisar_clientes
    2 - Pesquise os imóveis usando a ferramenta tool_retornar_imoveis_do_locador (por padrão, pesquise a página 1)
"""

pesquisando_contratos_do_locador = """
    Quando o usuário pedir os contratos de um locador
    1 - Identifique o código do locador pela ferramenta tool_pesquisar_clientes
    2 - Pesquise os contratos usando a ferramenta tool_retornar_contratos_do_locador (por padrão, pesquise a página 1)
"""

pesquisando_contratos_do_locatario = """
    Quando o usuário pedir os contratos de um locatario
    1 - Identifique o código do locatario pela ferramenta tool_pesquisar_clientes
    2 - Pesquise os contratos usando a ferramenta tool_retornar_contratos_do_locatario (por padrão, pesquise a página 1)
"""

prompts_list = [
    pesquisando_contratos_do_locador,
    pesquisando_imoveis_do_locador,
    pesquisando_contratos_do_locatario,
    pesquisando_um_repasse_pelo_locador    
]