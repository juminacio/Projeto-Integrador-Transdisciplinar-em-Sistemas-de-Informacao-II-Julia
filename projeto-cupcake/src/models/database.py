from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), default='cliente')

    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)
    carrinho = db.relationship('Carrinho', backref='usuario', lazy=True)


class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)  
    preco = db.Column(db.Float, nullable=False)        
    sabor = db.Column(db.String(50))                   
    disponivel = db.Column(db.Boolean, default=True)   
    imagem_url = db.Column(db.String(200), default='https://via.placeholder.com/150')


class Carrinho(db.Model):
    __tablename__ = 'carrinhos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    itens = db.relationship('ItemCarrinho', backref='carrinho', lazy=True)

class ItemCarrinho(db.Model):
    __tablename__ = 'itens_carrinho'
    
    id = db.Column(db.Integer, primary_key=True)
    carrinho_id = db.Column(db.Integer, db.ForeignKey('carrinhos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    
    produto = db.relationship('Produto')


class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow) 
    status = db.Column(db.String(50), default='Confirmado') 
    total = db.Column(db.Float, nullable=False) 

    itens = db.relationship('ItemPedido', backref='pedido', lazy=True)

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False) 
    

    produto = db.relationship('Produto')

