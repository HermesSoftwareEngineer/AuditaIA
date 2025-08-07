from pathlib import Path
import sqlite3, json
import ast
from .custom_types import Prompt

def carregar_prompts():
    db_path = Path(r"C:\Users\Hermes\PROJETOS_DEV\AuditaIA\src\models\data\prompts.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT title, description, prompt_text, context, tools FROM prompts")
    rows = cursor.fetchall()
    conn.close()

    prompts = []
    for row in rows:
        title, description, prompt_text, context, tools = row

        try:
            tools = ast.literal_eval(tools) if tools else []
        except Exception as e:
            print(f"[ERRO ao interpretar tools]: {tools}\n{e}")
            tools = []

        prompts.append(Prompt(
            title=title,
            description=description,
            prompt_text=prompt_text,
            context=context,
            tools=tools
        ))

    return prompts



def salvar_prompts_json(prompts_list, file_path):
    prompts_json = [
        {
            "title": p.title,
            "description": p.description,
            "prompt_text": p.prompt_text,
            "context": p.context,
            "tools": p.tools
        }
        for p in prompts_list
    ]

    caminho_json = Path(file_path)

    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(prompts_json, f, ensure_ascii=False, indent=2)

def carregar_e_salvar_prompts(file_path="prompts.json"):
    prompts_list = carregar_prompts()
    salvar_prompts_json(prompts_list, file_path)
    # print(f"Prompts carregados e salvos em {file_path}")
    return prompts_list