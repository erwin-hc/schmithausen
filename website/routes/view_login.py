from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from ..models.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from ..forms.forms_login import *
# ***********************************************************************************************
auth = Blueprint('auth', __name__)
# ***********************************************************************************************
# ENTRAR - LOGAR
# ***********************************************************************************************
@auth.route('/', methods=['GET', 'POST'])
def login():
    current_theme = session.get("theme")
    if current_theme == "":
        session["theme"] = "dark"

    logout_user()
    # ADICIONAR USUARIO ROOT      
    email_ja_existe = User.query.filter_by(email='adm@adm.com.br').first()
    if email_ja_existe == None:    
        root_user = User(email='adm@adm.com.br', first_name='ADMINISTRADOR', password=generate_password_hash(
        '123456', method='sha256')) 
        db.session.add(root_user)
        db.session.commit()
    # ADICIONAR CLIENTE DESCONHECIDO      
    fone_ja_existe = Cliente.query.filter_by(fone='(99) 9-9999-9999').first()
    if fone_ja_existe == None:    
        desconhecido = Cliente(nome='DESCONHECIDO', fone='(99) 9-9999-9999')
        db.session.add(desconhecido)
        db.session.commit()
    # -----------------------------------------------------------------------------------------------  
    # ADICIONAR PRODUTO TESTE
    existe_algum_produto = Produto.query.all()
    if existe_algum_produto == None:
        one = Produto(categoria='ESPETOS', descricao='ESPETO CONTRA-FILE', tamanho='100-G', valor=15, user_id=1)
        db.session.add(one)
        db.session.commit()  

    form=FormLogin()
    if form.validate_on_submit():  
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('senha')
            
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    return redirect(url_for('view_comandas.comandas'))
                else:
                    flash('SENHA INCORRETA !!!', category='error')
            else:
                flash('EMAIL NÃO CADASTRADO !!!', category='error')

    return render_template("entrar.html", form=form, user=current_user)
# ***********************************************************************************************
# SAIR - DESLOGAR
# ***********************************************************************************************
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
