from ai.custom_types import Prompt
import sqlite3
import os

def cadastrarPrompt(title, description, prompt_text, context, tools):
    print("Cadastrando prompt")
    prompt = Prompt(
        title=title,
        description=description,
        prompt_text=prompt_text,
        context=context,
        tools=tools
    )
    
    # Salvar no banco de dados SQLite
    data_dir = os.path.join(os.path.dirname(__file__), 'data')  # Ajuste: pasta data dentro de src
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, 'prompts.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            description TEXT,
            prompt_text TEXT,
            context TEXT,
            tools TEXT
        )
    ''')
    # Verifica se já existe um prompt com o mesmo título
    cursor.execute('SELECT id FROM prompts WHERE title = ?', (title,))
    if cursor.fetchone():
        conn.close()
        return {'sucess': False, 'description': "Prompt com esse título já existe. Não será cadastrado."}
    cursor.execute('''
        INSERT INTO prompts (title, description, prompt_text, context, tools)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, prompt_text, context, str(tools)))
    
    novoId = cursor.lastrowid

    conn.commit()
    conn.close()

    # Retorna um dicionário ao invés de um objeto Prompt
    return {
        "sucess": True,
        "content": {
            "id": novoId,
            "title": title,
            "description": description,
            "prompt_text": prompt_text,
            "context": context,
            "tools": tools
        }
    }

# def excluirPrompt(title)