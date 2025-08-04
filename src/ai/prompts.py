from .custom_types import Prompt
from pydantic import BaseModel
from typing import Literal
from .llms import llm

saudar_usuario_prompt = Prompt(
    title="saudar_usuario",
    description="Quando o usuário solicitar informações gerais.",
    prompt_text="PROMPT 2 = Quando o usuário solicitar informarções",
    context="saudacao",
    tools=[]
)

repasse_prompt = Prompt(
    title="pesquisar_repasse_locador",
    description="Quando o usuário solicitar informações sobre um repasse de um locador.",
    prompt_text="""
1. Utilize a ferramenta `tool_pesquisar_clientes` para obter o código do locador a partir do nome informado.
2. Solicite ao usuário o código do imóvel relacionado.
3. Solicite o mês desejado do repasse.
4. Solicite o ano correspondente.
5. Com todas as informações em mãos, use a ferramenta `tool_coletar_dados_repasse` para buscar os dados do repasse.
""",
    context="repasse",
    tools=["tool_pesquisar_clientes", "tool_coletar_dados_repasse"]
)

imoveis_locador_prompt = Prompt(
    title="pesquisar_imoveis_locador",
    description="Quando o usuário solicitar os imóveis vinculados a um locador.",
    prompt_text="""
1. Utilize a ferramenta `tool_pesquisar_clientes` para identificar o código do locador.
2. Use a ferramenta `tool_retornar_imoveis_do_locador` para buscar os imóveis associados (por padrão, inicie pela página 1).
""",
    context="imoveis_locador",
    tools=["tool_pesquisar_clientes", "tool_retornar_imoveis_do_locador"]
)

contratos_locador_prompt = Prompt(
    title="pesquisar_contratos_locador",
    description="Quando o usuário solicitar os contratos vinculados a um locador.",
    prompt_text="""
1. Utilize a ferramenta `tool_pesquisar_clientes` para identificar o código do locador.
2. Use a ferramenta `tool_retornar_contratos_do_locador` para buscar os contratos (por padrão, inicie pela página 1).
""",
    context="contratos_locador",
    tools=["tool_pesquisar_clientes", "tool_retornar_contratos_do_locador"]
)

contratos_locatario_prompt = Prompt(
    title="pesquisar_contratos_locatario",
    description="Quando o usuário solicitar os contratos vinculados a um locatário.",
    prompt_text="""
1. Utilize a ferramenta `tool_pesquisar_clientes` para identificar o código do locatário.
2. Use a ferramenta `tool_retornar_contratos_do_locatario` para buscar os contratos (por padrão, inicie pela página 1).
""",
    context="contratos_locatario",
    tools=["tool_pesquisar_clientes", "tool_retornar_contratos_do_locatario"]
)

prompts_list = [
    saudar_usuario_prompt,
    repasse_prompt,
    imoveis_locador_prompt,
    contratos_locador_prompt,
    contratos_locatario_prompt
]

prompt_index = [
    {
        "title": p.title,
        "description": p.description,
        "context": p.context,
        "tools": p.tools,
        "text": p.prompt_text
    }
    for p in prompts_list
]

titulosValidos = [
    p.title for p in prompts_list
]

PromptTitle = Literal[tuple(titulosValidos)]

class PromptChoice(BaseModel):
    title: PromptTitle