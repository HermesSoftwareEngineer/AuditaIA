from pydantic import BaseModel
from typing import Literal
import json
from pathlib import Path
from .custom_types import Prompt

def carregar_prompts_do_json(file_path: str | Path = "prompts.json") -> list[Prompt]:
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo JSON não encontrado: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [Prompt(**item) for item in data]

prompts_list = carregar_prompts_do_json()

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

titulosValidos = [p.title for p in prompts_list]

# Literal e modelo definido uma vez
PromptTitle = Literal[tuple(titulosValidos)]

class PromptChoice(BaseModel):
    title: PromptTitle
