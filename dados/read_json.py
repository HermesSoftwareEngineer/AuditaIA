import json
import pandas as pd
from sqlalchemy import create_engine

# Carrega o JSON (substitua pelo caminho real do arquivo)
with open(r'dados/movimentos.json', encoding='utf-8') as f:
    data = json.load(f)

# Inicializa listas para os dados principais e os detalhes
movimentos = []
detalhes = []

# Percorre os movimentos e separa os dados
for item in data['lista']:
    movimento_id = item['codigo']
    
    # Copia o item original e remove os campos que vão virar tabela separada
    movimento = item.copy()
    detalhes_raw = movimento.pop('detalhes', [])
    
    # Remove outros campos que são listas se você não quiser armazená-los agora
    movimento.pop('formasquitacao', None)
    movimento.pop('repasses', None)
    
    # Adiciona o movimento à lista principal
    movimentos.append(movimento)
    
    # Extrai os detalhes com referência ao código do movimento
    for detalhe in detalhes_raw:
        detalhe['movimento_id'] = movimento_id
        detalhes.append(detalhe)

# Converte listas em DataFrames
df_movimentos = pd.DataFrame(movimentos)
df_detalhes = pd.DataFrame(detalhes)

# Cria conexão com o banco (SQLite local, substitua se quiser)
engine = create_engine('sqlite:///movimentos.db')

# Salva no banco de dados
df_movimentos.to_sql('movimentos', con=engine, if_exists='replace', index=False)
df_detalhes.to_sql('detalhes', con=engine, if_exists='replace', index=False)

print("Tabelas 'movimentos' e 'detalhes' salvas com sucesso.")
