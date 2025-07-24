from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt_coletor = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                Utilize a ferramenta para coletar os dados necessários para responder ao usuário!
            """
        ),
        MessagesPlaceholder(variable_name='messages')
    ]
)

prompt_assistente = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                Você é um assistente virtual de consulta ligado ao sistema da Imobiliária. Ajude os usuários da Imobiliária Stylus fornecedendo os dados pedidos. Verifique se deve responde diretamente ou coletar dados.

                Analise cuidadosamente todas as ferramentas disponíveis no seu ambiente atual. Aproveite ao máximo os recursos acessíveis para trabalhar com o que já está disponível no contexto, histórico ou ambiente.
            """
        ),
        MessagesPlaceholder(variable_name='messages')
    ]
)

prompt_consultor = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                
                Se estiver faltando algum dado, pode perguntar ao usuário.
            """
        ),
        MessagesPlaceholder(variable_name='messages')
    ]
)

prompt_selector = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Identifique o prompt mais apropriado que servirá como instrução pro agent executor"""
        ),
        MessagesPlaceholder(variable_name='messages')
    ]
)

planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Elabore um plano de utilização de ferramentas pra conseguir os dados necessário para cumprir o objetivo informado.
            Ferramentas disponíveis:
            - tool_coletar_dados_repasse: coleta dados de repasse. Parametros necessários: codigoCliente: int, codigoImovel: int, ano: int, mes: int
            - tool_pesquisar_clientes: pesquisa o cliente e descobre o código dele. Parametros necessários: textoPesquisa: str
            - tool_retornar_imoveis_do_locador: 
            - tool_retornar_contratos_do_locador
            - tool_retornar_contratos_do_locatario
            """
        ),
        MessagesPlaceholder(variable_name="input")
    ]
)