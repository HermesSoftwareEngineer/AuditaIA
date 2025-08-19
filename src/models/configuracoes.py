from ai.auditing_agent.custom_types import Prompt
import sqlite3
import json
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

def excluirPrompt(id):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, 'prompts.db')
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM prompts WHERE id = ?", (id,))

    prompt = cursor.fetchone()

    if not prompt:
        return {'sucess': False, 'content': {
            'erro': 'Prompt não encontrado!'
        }}

    cursor.execute("DELETE FROM prompts WHERE id = ?", (id,))

    conn.commit()

    if cursor.rowcount == 0:
        return {'sucess': False, 'content': {
            'erro': 'Erro ao excluir prompt!'
        }}
    
    return {
        'sucess': True,
        'content': {
            'id': id,
            # ADICIONAR MAIS CAMPOS AQUI
        }
    }

def listar_prompts():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, 'prompts.db')
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM prompts")

    prompts_list = cursor.fetchall()

    if not prompts_list:
        return {'sucess': False, 'erro': {
            'erro': 'Prompts não encontrados!'
        }}
    
    return {
        'sucess': True,
        'content': prompts_list
    }

def atualizarPrompt(id, title, description, prompt_text, context, tools):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, 'prompts.db')
    conn = None 
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Primeiro, verificamos se o prompt existe para evitar a execução desnecessária do UPDATE
        cursor.execute("SELECT * FROM prompts WHERE id = ?", (id,))
        prompt = cursor.fetchone()
        
        if not prompt:
            return {'success': False, 'description': 'Prompt não encontrado!'}
        
        # Converte 'tools' para string JSON para armazenamento seguro
        tools_str = json.dumps(tools)

        # Executa o UPDATE de forma segura com placeholders
        cursor.execute('''
            UPDATE prompts
            SET title = ?, description = ?, prompt_text = ?, context = ?, tools = ?
            WHERE id = ?
        ''', (title, description, prompt_text, context, tools_str, id))

        conn.commit()

        # A verificação de sucesso pode ser feita logo após o commit
        if cursor.rowcount > 0:
             return {
                'success': True,
                'content': {
                    'title': title,
                    'description': description,
                    'prompt_text': prompt_text,
                    'context': context,
                    'tools': tools
                }
            }
        else:
            # Caso o UPDATE não tenha afetado nenhuma linha (situação improvável aqui)
            return {'success': False, 'erro': 'Erro ao atualizar prompt!'}
            
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        return {'success': False, 'erro': f'Erro no banco de dados: {e}'}
    finally:
        if conn:
            conn.close()