import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    # Cria pasta logs se não existir
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Cria um handler que rotaciona o arquivo de log (evita arquivos gigantes)
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        )
    )
    file_handler.setLevel(logging.INFO)  # pode mudar para DEBUG em dev

    # Conecta no logger do Flask
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
