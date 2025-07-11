from flask import Flask, request
from .routes import bot

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.register_blueprint(bot.bp)

    return app