from flask import Flask, render_template,request,redirect,Blueprint,url_for
from utils import db, lm
from flask_migrate import Migrate
from models import Peca,Usuario,Pedido
from routes.home import home_route
from routes.peca import peca_route
from routes.usuario import usuario_route

app = Flask(__name__)
app.secret_key = "Minha_chave_Secreta"

conexao = "sqlite:///meubanco.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = False

db.init_app(app)
lm.init_app(app)
migrate = Migrate(app,db)

app.register_blueprint(home_route)
app.register_blueprint(peca_route,url_prefix='/pecas')
app.register_blueprint(usuario_route,url_prefix='/usuario')

@lm.unauthorized_handler
def unauthorized():
    return redirect(url_for('usuario.login'))




if __name__ == '__main__':
    app.run()
