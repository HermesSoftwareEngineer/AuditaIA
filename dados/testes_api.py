from request_api import consultar_repasse_locador
import json

dados = consultar_repasse_locador("01/02/2025", "28/02/2025", 90)

# Criando o arquivo JSON
with open("dados.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados, arquivo, ensure_ascii=False, indent=4)