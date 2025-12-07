from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializa o objeto do banco de dados
db = SQLAlchemy()

# ---------------------------------------------------------
# CLASSE USUÁRIO
# Baseado no Diagrama de Classes (Pág. 23) [cite: 484]
# ---------------------------------------------------------
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)   # [cite: 486]
    email = db.Column(db.String(100), unique=True, nullable=False) # [cite: 487]
    senha = db.Column(db.String(100), nullable=False)  # [cite: 488]
    tipo = db.Column(db.String(20), default='cliente') # [cite: 489] (cliente ou admin)

    # Relacionamentos (Não criam colunas, mas facilitam o acesso no Python)
    # Um usuário pode ter vários pedidos
    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)
    # Um usuário tem carrinhos (definido como 0..* no diagrama [cite: 483])
    carrinho = db.relationship('Carrinho', backref='usuario', lazy=True)


# ---------------------------------------------------------
# CLASSE PRODUTO (CUPCAKE)
# Baseado no Diagrama de Classes (Pág. 23) [cite: 513]
# ---------------------------------------------------------
class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)   # [cite: 515]
    preco = db.Column(db.Float, nullable=False)        # [cite: 516]
    sabor = db.Column(db.String(50))                   # [cite: 517]
    disponivel = db.Column(db.Boolean, default=True)   # [cite: 518]
    
    # Campo extra para funcionar no site (mostrar a foto do wireframe [cite: 572])
    imagem_url = db.Column(db.String(200), default='https://via.placeholder.com/150')


# ---------------------------------------------------------
# CLASSES DO CARRINHO DE COMPRAS
# Baseado no Diagrama de Classes (Pág. 23) [cite: 492, 502]
# ---------------------------------------------------------
class Carrinho(db.Model):
    __tablename__ = 'carrinhos'
    
    id = db.Column(db.Integer, primary_key=True)
    # Chave estrangeira ligando ao Usuário [cite: 495]
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Lista de itens dentro deste carrinho
    itens = db.relationship('ItemCarrinho', backref='carrinho', lazy=True)

class ItemCarrinho(db.Model):
    __tablename__ = 'itens_carrinho'
    
    id = db.Column(db.Integer, primary_key=True)
    # Ligações com Carrinho e Produto [cite: 504]
    carrinho_id = db.Column(db.Integer, db.ForeignKey('carrinhos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    
    # Facilita acessar os dados do produto (nome, preço) a partir do item
    produto = db.relationship('Produto')


# ---------------------------------------------------------
# CLASSES DE PEDIDOS (CHECKOUT)
# Baseado no Diagrama de Classes (Pág. 23) [cite: 498, 507]
# ---------------------------------------------------------
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow) # [cite: 499]
    status = db.Column(db.String(50), default='Confirmado') # [cite: 499]
    total = db.Column(db.Float, nullable=False)            # [cite: 499]

    # Lista de itens deste pedido
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True)

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    # Ligações com Pedido e Produto [cite: 509]
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False) # Importante para histórico [cite: 510]
    
    produto = db.relationship('Produto')