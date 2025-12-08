import os
from werkzeug.utils import secure_filename
from flask import current_app
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import db, Usuario, Produto, Carrinho, ItemCarrinho


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():

    produtos = Produto.query.filter_by(disponivel=True).all()
    return render_template('home.html', produtos=produtos)



@main_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')


        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Este e-mail já está cadastrado.')
            return redirect(url_for('main.registro'))


        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Conta criada com sucesso! Faça login.')
        return redirect(url_for('main.login'))

    return render_template('registro.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.senha == senha:
            session['user_id'] = usuario.id
            session['user_nome'] = usuario.nome
            return redirect(url_for('main.index'))
        else:
            flash('Email ou senha incorretos.')
    
    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_nome', None)
    return redirect(url_for('main.index'))

# --- ROTAS DO CARRINHO DE COMPRAS ---

@main_bp.route('/adicionar_carrinho/<int:produto_id>')
def adicionar_carrinho(produto_id):
    if 'user_id' not in session:
        flash('Faça login para comprar.')
        return redirect(url_for('main.login'))

    usuario_id = session['user_id']
    

    carrinho = Carrinho.query.filter_by(usuario_id=usuario_id).first()
    if not carrinho:
        carrinho = Carrinho(usuario_id=usuario_id)
        db.session.add(carrinho)
        db.session.commit()

    item = ItemCarrinho.query.filter_by(carrinho_id=carrinho.id, produto_id=produto_id).first()
    if item:
        item.quantidade += 1
    else:
        novo_item = ItemCarrinho(carrinho_id=carrinho.id, produto_id=produto_id, quantidade=1)
        db.session.add(novo_item)
    
    db.session.commit()
    flash('Produto adicionado ao carrinho!')
    return redirect(url_for('main.index'))

@main_bp.route('/carrinho')
def ver_carrinho():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    usuario_id = session['user_id']
    carrinho = Carrinho.query.filter_by(usuario_id=usuario_id).first()
    
    itens = []
    total = 0
    if carrinho:
        itens = carrinho.itens
        for item in itens:
            total += item.produto.preco * item.quantidade

    return render_template('carrinho.html', itens=itens, total=total)

@main_bp.route('/remover_item/<int:item_id>')
def remover_item(item_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
        
    item = ItemCarrinho.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Item removido.')
    
    return redirect(url_for('main.ver_carrinho'))
    
@main_bp.route('/admin/adicionar', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = float(request.form.get('preco'))
        sabor = request.form.get('sabor')
        

        arquivo = request.files.get('imagem')
        caminho_imagem = '' 

        if arquivo and arquivo.filename != '':
            nome_arquivo = secure_filename(arquivo.filename)
            caminho_completo = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_arquivo)
            arquivo.save(caminho_completo)
            caminho_imagem = nome_arquivo
        else:
            caminho_imagem = 'https://via.placeholder.com/300'

        novo_produto = Produto(
            nome=nome, 
            preco=preco, 
            sabor=sabor, 
            imagem_url=caminho_imagem
        )
        
        db.session.add(novo_produto)
        db.session.commit()
        
        flash('Cupcake adicionado com sucesso!')
        return redirect(url_for('main.index'))


    return render_template('adicionar_produto.html')
