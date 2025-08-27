from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users' 
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default='user')  # 'admin' ou 'user'
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.user_type == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'
