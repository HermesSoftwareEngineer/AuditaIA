import os
from datetime import timedelta

class ProductionConfig:
    # Database - Render PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', os.environ.get('SECRET_KEY'))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Flask
    DEBUG = False
    TESTING = False
    
    # CORS - Render específico
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Render específico
    PORT = int(os.environ.get('PORT', 10000))
    HOST = '0.0.0.0'    
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/auditaia.log'
    
    # SSL redirect para HTTPS no Render
    PREFERRED_URL_SCHEME = 'https'
    
    # Session config
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
