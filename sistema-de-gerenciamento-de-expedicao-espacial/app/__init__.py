from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
from app.models.missoes import Missoes
with app.app_context():
    db.create_all()

from app.view.reso_missoes import Index, Cria_missao, Atualiza_missao, Deleta_missao, Visualizar_missao, Visualizar_id, Visualizar_data
api.add_resource(Index, '/')
api.add_resource(Cria_missao, '/criar')
api.add_resource(Atualiza_missao, '/atualizar')
api.add_resource(Deleta_missao, '/deletar')
api.add_resource(Visualizar_missao, '/visualizar')
api.add_resource(Visualizar_id, '/visualizar/<int:id>')
api.add_resource(Visualizar_data, '/visualizar_data') #coloque /visualizar_data?data_inicio=ano-mes-dia&data_fim=ano-mes-dia para visualizar entre um intervalo de datas