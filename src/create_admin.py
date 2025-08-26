from app import create_app
from app.models.user import User, db

app = create_app()

def create_initial_admin():
    with app.app_context():
        # Verificar se já existe algum admin
        admin = User.query.filter_by(user_type='admin').first()
        
        if not admin:
            # Criar um admin inicial
            admin = User(
                username='admin',
                email='admin@example.com',
                user_type='admin'
            )
            admin.set_password('admin123')  # Troque por uma senha mais segura em produção
            
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário admin criado com sucesso!")
            print("Username: admin")
            print("Senha: admin123")
        else:
            print("⚠️ Já existe pelo menos um usuário admin no sistema.")

if __name__ == "__main__":
    create_initial_admin()
