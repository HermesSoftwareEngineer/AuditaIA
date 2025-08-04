from flask import Flask, request
from .routes import bot, configuracoes
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    CORS(app, resources={
        r"/v1/*": {
            "origins": os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
        }
    })

    app.register_blueprint(bot.bp)
    app.register_blueprint(configuracoes.bp)
    app.config['JSON_SORT_KEYS'] = False
    
    return app