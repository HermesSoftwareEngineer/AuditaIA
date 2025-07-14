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