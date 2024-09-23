from flask import Blueprint,render_template,request,redirect,url_for,flash
from utils import db, lm
from models import Usuario
from flask_login import login_user,logout_user,login_required

usuario_route = Blueprint('usuario',__name__)


@usuario_route.route('/')
@login_required
def listagem_usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('listar_usuarios.html', lista=lista_usuarios)

@usuario_route.route('/cadastrar', methods=['GET','POST'])
@login_required
def cadastrar_usuario():
    if request.method == 'GET':
        return render_template('cadastrar_usuario.html')
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']

        u = Usuario(nome, email)

        db.session.add(u)
        db.session.commit()
        
        return redirect(url_for('usuario.listagem_usuarios'))

@usuario_route.route('/editar/<int:id_usuario>')
@login_required
def editar(id_usuario):
    
    p = Usuario.query.get(id_usuario)
    
    return render_template('editar_usuario.html',dados_usuario=p) 

@usuario_route.route('/editar_enviar', methods=['POST'])
@login_required
def editar_enviar():
    id_usuario = request.form['id_usuario']
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    
    u = Usuario.query.get(id_usuario)
    u.nome = nome
    u.email= email 
    u.senha = senha

    db.session.add(u)
    db.session.commit()
    
    

    return redirect(url_for('usuario.listagem_usuarios'))

@usuario_route.route('/excluir/<int:id_usuario>')
#@login_required
def excluir(id_usuario):
    u = Usuario.query.get(id_usuario)
    
    db.session.delete(u)
    db.session.commit()
    
    return redirect(url_for('usuario.listagem_usuarios'))

@lm.user_loader
def load_user(id):
    usuario = Usuario.query.filter_by(id=id).first()
    return usuario

@usuario_route.route('/autenticar', methods=['POST'])
def autenticar ():
    email = request.form.get('email')
    senha = request.form.get('senha')
    usuario = Usuario.query.filter_by(email=email).first()
    
    if (usuario and (senha == usuario.senha)):
        login_user(usuario)
        return redirect (url_for('home.home'))
    else:
        flash('Dados incorretos')
        return redirect(url_for('home.home'))
    
@usuario_route.route('/login')
def login():
    return render_template ('login.html')

@usuario_route.route('/login')
def logoff():
    logout_user()
    return redirect(url_for('usuario.login'))