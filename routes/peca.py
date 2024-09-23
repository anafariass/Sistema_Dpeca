from flask import Blueprint,render_template,request,redirect,url_for,flash 
from utils import db
from models import Peca

peca_route = Blueprint('peca',__name__)

@peca_route.route('/')
def listagem_pecas():
    lista_pecas = Peca.query.all()
    return render_template('listagem_pecas.html', lista=lista_pecas)

@peca_route.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar_peca.html')

@peca_route.route('/cadastrar_enviar', methods = {'POST'})
def cadastrar_enviar():
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    
    valor = request.form['valor']
    
    p = Peca(nome,quantidade,valor)
    
    db.session.add(p)
    db.session.commit()

    flash('Peça cadastrada com sucesso!',"success")
    
    return redirect(url_for('peca.listagem_pecas'))

@peca_route.route('/editar/<int:id_peca>')
def editar(id_peca):
    
    p = Peca.query.get(id_peca)
    
    return render_template('editar_pecas.html',dados_peca=p) 

@peca_route.route('/editar_enviar', methods=['POST'])
def editar_enviar():
    id_peca = request.form['id_peca']
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    valor = request.form['valor']
    
    p = Peca.query.get(id_peca)
    p.nome= nome
    p.quantidade= quantidade 
    p.valor= valor 
    
    db.session.add(p)
    db.session.commit()
    
    flash('Peça editada com sucesso!',"success")

    return redirect(url_for('peca.listagem_pecas'))

@peca_route.route('/excluir/<int:id_peca>')
def excluir(id_peca):
    p = Peca.query.get(id_peca)
    
    db.session.delete(p)
    db.session.commit()

    flash('Peça excluída com sucesso!',"danger")
    
    return redirect(url_for('peca.listagem_pecas'))
