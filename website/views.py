from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import *
from .forms import *
import datetime
import json

# ***********************************************************************************************
# DATA ATUAL
# ***********************************************************************************************
data = x = datetime.datetime.now().date()
# ***********************************************************************************************
views = Blueprint('views', __name__)
# ***********************************************************************************************
# COMANDAS
# ***********************************************************************************************
@views.route('/comandas', methods=['GET', 'POST'])
@login_required
def comandas():
    return render_template("comandas.html", user=current_user, data=data)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
# USUARIOS   
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    
# ***********************************************************************************************
# USUARIOS -- LISTAR
# ***********************************************************************************************
@views.route('/usuarios', methods=['GET','POST'])
@login_required
def usuarios():
    users = []
    rows = User.query.all()
    for r in rows:
        users.append(r)   
    return render_template("usuarios_listar.html", user=current_user, data=data, users=users)
# ***********************************************************************************************
# USUARIOS -- CADASTRAR
# ***********************************************************************************************
@views.route('/usuarios_cadastrar', methods=['GET','POST'])
@login_required
def cadastroUsuarios():
    form = CadastroUsuario()
    if form.validate_on_submit():
        if request.method == 'POST':
            email = request.form.get('email')
            first_name = request.form.get('nome')
            password1 = request.form.get('senha')
            password2 = request.form.get('confirmar')
            user = User.query.filter_by(email=email).first()
            if user:
                flash('EMAIL JÁ CADASTRADO!', category='error')
                return redirect(url_for('views.cadastroUsuarios'))
            else:
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
            return redirect(url_for('views.usuarios'))
    return render_template("usuarios_cadastrar.html", user=current_user, data=data, form=form)
# ***********************************************************************************************
# USUARIOS -- DELETAR
# ***********************************************************************************************
@views.route('/usuarios_deletar/<int:id>', methods=['POST','GET'])
def deletarUsuario(id):  
    get_users = User.query.get(id)
    if id == 1:
        flash('NÃO PODE SER EXCLUÍDO!',category='error')
    else:
        if get_users:
            db.session.delete(get_users)
            db.session.commit()
            return redirect(url_for('views.usuarios'))
    return redirect(url_for('views.usuarios'))
# ***********************************************************************************************
# USUARIOS -- ATUALIZAR
# ***********************************************************************************************
@views.route('/usuarios_atualizar/<int:id>', methods=['GET','POST'])
@login_required
def atualizarUsuarios(id): 
    form = CadastroUsuario()
    get_users = User.query.get(id)
    if request.method == 'GET':        
        if id != 1:
            return render_template('usuarios_atualizar.html', 
                user=current_user, 
                data=data, 
                form=form,
                u=get_users
                )
        else:
            flash('NÃO PODE SER EDITADO!')
            return redirect(url_for('views.usuarios'))
    if form.validate_on_submit():        
        if request.method == 'POST':
            email = request.form.get('email')
            email_ja_existe = User.query.filter_by(email=email).first()
            if email_ja_existe == None or email_ja_existe.id == id:
                nome = request.form.get('nome')
                email = request.form.get('email')
                get_users.first_name = nome
                get_users.email = email 
                db.session.commit()
            else:
                flash('EMAIL JÁ CADASTRADO!', category='error')
                return render_template('usuarios_atualizar.html', 
                    user=current_user, 
                    data=data, 
                    form=form,
                    u=get_users
                    )   
    else:    
        return render_template('usuarios_atualizar.html', 
                user=current_user, 
                data=data, 
                form=form,
                u=get_users
                ) 
    return redirect(url_for('views.usuarios'))
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
# CLIENTES   
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    
# ***********************************************************************************************
# CLIENTES -- LISTAR
# ***********************************************************************************************
@views.route('/clientes', methods=['GET','POST'])
@login_required
def clientes():
    clientes = []
    rows = Cliente.query.all()
    for r in rows:
        clientes.append(r)        
    return render_template("clientes_listar.html", user=current_user, data=data, clientes=clientes)
# ***********************************************************************************************
# CLIENTES -- CADASTRAR
# ***********************************************************************************************
@views.route('/clientes_cadastrar', methods=['GET','POST'])
@login_required
def cadastroClientes():
    form = CadastroCliente()
    if form.validate_on_submit():
        if request.method == 'POST':
            nome = request.form.get('nome').upper()
            fone = request.form.get('fone')
            existis_fone = Cliente.query.filter_by(fone=fone).first()
            if existis_fone:
                flash('CELULAR JÁ CADASTRADO !!!', category='error')
            else:
                novo_cliente = Cliente(nome=nome, fone=fone)
                db.session.add(novo_cliente)
                db.session.commit()   
                return redirect(url_for('views.clientes'))
    return render_template("clientes_cadastrar.html", user=current_user, data=data, form=form)
# ***********************************************************************************************
# CLIENTES -- DELETAR
# ***********************************************************************************************
@views.route('/clientes_deletar/<int:id>', methods=['POST', 'GET'])
@login_required
def deletarCliente(id):
    get_cli = Cliente.query.get(id)
    if id == 1:
        flash('NÃO PODE SER EXCLUÍDO!',category='error')
    else:
        if get_cli:
            db.session.delete(get_cli)
            db.session.commit()
            return redirect(url_for('views.clientes'))
    return redirect(url_for('views.clientes'))
# ***********************************************************************************************
# CLIENTES -- ATUALIZAR
# ***********************************************************************************************
@views.route('/clientes_atualizar/<int:id>', methods=['GET','POST'])
@login_required
def atualizarClientes(id): 
    form = CadastroCliente()
    get_cli = Cliente.query.get(id)
    if request.method == 'GET':
        if id != 1:
            return render_template('clientes_atualizar.html', 
                user=current_user, 
                data=data, 
                form=form,
                c=get_cli
                )
        else:
            flash('NÃO PODE SER EDITADO!')
            return redirect(url_for('views.clientes'))    
    if form.validate_on_submit():
        if request.method == 'POST':
            nome = request.form.get('nome').upper()
            fone = request.form.get('fone')
            existis_fone = Cliente.query.filter_by(fone=fone).first()
            if existis_fone == None or existis_fone.id == id:
                get_cli.nome = nome
                get_cli.fone = fone
                db.session.commit()
            else:
                flash('CELULAR JÁ CADASTRADO !!!', category='error')
                return render_template('clientes_atualizar.html', 
                    user=current_user, 
                    data=data, 
                    form=form,
                    c=get_cli
                    )  
    else:
        return render_template('clientes_atualizar.html', 
            user=current_user, 
            data=data, 
            form=form,
            c=get_cli
            )
    return redirect(url_for('views.clientes'))
    
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
# PRODUTOS   
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    
# ***********************************************************************************************
# PRODUTOS -- LISTAR
# ***********************************************************************************************
@views.route('/produtos', methods=['GET','POST'])
@login_required
def produtos():
    produtos = Produto.query.all()
    tamanhos = Tamanho.query.all()
    categorias = Categoria.query.all()
    return render_template("produtos_listar.html", 
        user=current_user,
        data=data, 
        produtos=produtos,
        tamanhos=tamanhos,
        categorias=categorias)        
# ***********************************************************************************************
# PRODUTOS -- CADASTRAR
# ***********************************************************************************************
@views.route('/produtos_cadastrar', methods=['POST','GET'])
@login_required
def cadastroProdutos():
    form = CadastroProduto()
    form.categoria.query = Categoria.query 
    form.tamanho.query = Tamanho.query
    espetos =  db.session.query(Tamanho).join(Categoria).filter(Categoria.id == 1).all()
    objTamanhos = Tamanho.query.all()
    catArray = []
    for row in objTamanhos:
        obj = {}
        obj['tam_id'] = row.id
        obj['tam_nome'] = row.nome
        obj['cat_id'] = row.tamanhos.id
        obj['cat_nome'] = row.tamanhos.nome
        catArray.append(obj)
    if form.validate_on_submit():
        if request.method == 'POST':
            categoria = request.form.get('categoria')
            tamanho = request.form.get('tamanho')
            descricao = request.form.get('descricao').upper()   
            valor = float(request.form.get('valor').replace(",","."))
            criador = current_user.id
            novo_produto = Produto(categoria=categoria,tamanho=tamanho,descricao=descricao,valor=valor,user_id=criador)
            db.session.add(novo_produto)
            db.session.commit()
            return redirect(url_for('views.produtos'))
        else:
            return render_template('produtos_cadastrar.html',
                user=current_user,
                data=data, 
                form=form,
                espetos=espetos,
                objTamanhos=catArray)            
    return render_template('produtos_cadastrar.html',
        user=current_user,
        data=data, 
        form=form,
        espetos=espetos,
        objTamanhos=catArray)
# @views.route('/categoria/<int:id>')
# def categoria(id):
#     tam = Tamanho.query.filter_by(cat_id=id).all()
#     newArray = [{'valor':0, 'nome':'-- SELECIONE --'}]
#     for row in tam:
#         obj = {}
#         obj['valor'] = row.id
#         obj['nome'] = row.nome
#         newArray.append(obj)
#     return newArray
# ***********************************************************************************************
# PRODUTOS -- DELETAR
# ***********************************************************************************************
@views.route('/produtos_deletar/<int:id>', methods=['POST','GET'])
def deletarProduto(id):  
    get_produto = Produto.query.get(id)
    if get_produto:
        db.session.delete(get_produto)
        db.session.commit()
    return redirect(url_for('views.produtos'))
# ***********************************************************************************************
# PRODUTOS -- ATUALIZAR
# ***********************************************************************************************
@views.route('/produtos_atualizar/<int:id>/<int:cat>/<int:tam>', methods=['GET','POST'])
@login_required
def atualizarProdutos(id,cat,tam):
    form = CadastroProduto()
    form.categoria.query = Categoria.query 
    form.tamanho.query = Tamanho.query
    get_pro = Produto.query.get(id)
    
    objTamanhos = Tamanho.query.all()
    catArray = []
    for row in objTamanhos:
        obj = {}
        obj['tam_id'] = row.id
        obj['tam_nome'] = row.nome
        obj['cat_id'] = row.tamanhos.id
        obj['cat_nome'] = row.tamanhos.nome
        catArray.append(obj)
  
    get_cat_text = Categoria.query.get(cat).nome
    get_tam_text = Tamanho.query.get(tam).nome

    if form.validate_on_submit():
        if request.method == 'POST':
            categoria = request.form.get('categoria')
            tamanho = request.form.get('tamanho')
            descricao = request.form.get('descricao').upper()   
            valor = float(request.form.get('valor').replace(",","."))
            criador = current_user.id
            get_pro.categoria = categoria
            get_pro.tamanho = tamanho
            get_pro.descricao = descricao
            get_pro.valor = valor
            db.session.commit()
            return redirect(url_for('views.produtos'))


    return render_template('produtos_atualizar.html', 
    user=current_user, 
    data=data, 
    form=form,
    p=get_pro,
    objTamanhos=catArray,
    tamTex=get_tam_text,
    catTex=get_cat_text
    )


# ***********************************************************************************************
# TOOGLE-THEME
# ***********************************************************************************************
@views.route("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "light":
        session["theme"] = "dark"
    else:
        session["theme"] = "light"

    return redirect(request.args.get("current_page"))

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
# CATEGORIAS   
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    
# ***********************************************************************************************
# CATEGORIAS -- LISTAR
# ***********************************************************************************************
@views.route('/categorias', methods=['GET','POST'])
@login_required
def categorias():
    categorias = Categoria.query.all()
    tamanhos = Tamanho.query.all()
    print(categorias)
    return render_template("categorias_listar.html", 
        user=current_user,
        data=data, 
        tamanhos=tamanhos,
        categorias=categorias)