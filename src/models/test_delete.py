import sqlite3
import os

def delete_first_row():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')  # Ajuste: pasta data dentro de src
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, 'prompts.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM prompts WHERE id = 1")
        conn.commit()
        print("Primeira linha excluída com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao excluir: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    delete_first_row()