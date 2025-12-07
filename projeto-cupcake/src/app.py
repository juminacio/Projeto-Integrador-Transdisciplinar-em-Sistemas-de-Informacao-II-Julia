import os # <--- IMPORTANTE: Necessário para lidar com pastas
from flask import Flask
from models.database import db
from controllers.routes import main_bp

def create_app():
    # Define as pastas de templates e estáticos
    app = Flask(__name__, template_folder='views/templates', static_folder='views/static')

    # --- CONFIGURAÇÃO DO BANCO DE DADOS ---
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cupcake.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'minha-chave-super-secreta-pit2'

    # --- CONFIGURAÇÃO DE UPLOAD (O QUE ESTAVA FALTANDO) ---
    # 1. Descobre onde este arquivo app.py está no computador
    basedir = os.path.abspath(os.path.dirname(__file__)) 
    
    # 2. Define o caminho: src/views/static/uploads
    upload_path = os.path.join(basedir, 'views', 'static', 'uploads')
    
    # 3. Salva essa configuração no Flask para o routes.py usar
    app.config['UPLOAD_FOLDER'] = upload_path
    
    # 4. Cria a pasta física no computador se ela não existir
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    # -----------------------------------------------------

    # Inicializa o Banco e as Rotas
    db.init_app(app)
    app.register_blueprint(main_bp)

    # Cria as tabelas se não existirem
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)