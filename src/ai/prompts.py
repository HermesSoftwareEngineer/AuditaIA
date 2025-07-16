from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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
                Você é um assistente auditor e ajuda a uma imobiliária a verificar e auditar prestações de contas. Verifique se deve responde diretamente ou coletar dados.
            """
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