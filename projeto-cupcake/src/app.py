import os 
from flask import Flask
from models.database import db
from controllers.routes import main_bp

def create_app():
    app = Flask(__name__, template_folder='views/templates', static_folder='views/static')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cupcake.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'minha-chave-super-secreta-pit2'

    basedir = os.path.abspath(os.path.dirname(__file__)) 

    upload_path = os.path.join(basedir, 'views', 'static', 'uploads')

    app.config['UPLOAD_FOLDER'] = upload_path

    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    db.init_app(app)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()

    app.run(debug=True)
