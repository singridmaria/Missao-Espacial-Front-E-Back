from flask import jsonify, request
from flask_restful import Resource, reqparse
from app.models.missoes import Missoes
from datetime import datetime

#para criar
argumentos_criacao = reqparse.RequestParser()#definir os argumentos da solicitação HTTP
argumentos_criacao.add_argument('id', type=int)
argumentos_criacao.add_argument('nome_missao', type=str)
argumentos_criacao.add_argument('data_lancamento', type=str)
argumentos_criacao.add_argument('destino', type=str)
argumentos_criacao.add_argument('estado_missao', type=str)
argumentos_criacao.add_argument('tripulacao', type=str)
argumentos_criacao.add_argument('carga_util', type=str)
argumentos_criacao.add_argument('duracao_missao', type=str)
argumentos_criacao.add_argument('custo_missao', type=float)
argumentos_criacao.add_argument('status_missao', type=str)

#para atualizar
argumentos_atualizacao = reqparse.RequestParser()#definir os argumentos da solicitação HTTP
argumentos_atualizacao.add_argument('id', type=int)
argumentos_atualizacao.add_argument('nome_missao', type=str)
argumentos_atualizacao.add_argument('data_lancamento', type=str)
argumentos_atualizacao.add_argument('destino', type=str)
argumentos_atualizacao.add_argument('estado_missao', type=str)
argumentos_atualizacao.add_argument('tripulacao', type=str)
argumentos_atualizacao.add_argument('carga_util', type=str)
argumentos_atualizacao.add_argument('duracao_missao', type=str)
argumentos_atualizacao.add_argument('custo_missao', type=float)
argumentos_atualizacao.add_argument('status_missao', type=str)

#para deletar
argumentos_exclusao = reqparse.RequestParser()
argumentos_exclusao.add_argument('id', type=int)

class Index(Resource):
    def get(self):
        return jsonify("Welcome Aplication Flask")

class Cria_missao(Resource):
    def post(self):
        try:
            datas = argumentos_criacao.parse_args()
            Missoes.salva_missao(self,datas['nome_missao'],datas['data_lancamento'],datas['destino'],datas['estado_missao'],datas['tripulacao'],datas['carga_util'],datas['duracao_missao'],datas['custo_missao'],datas['status_missao'])
            return {"message": 'Missão criada com sucesso!'}, 200
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class Atualiza_missao(Resource):
    def put(self):
        try:
            datas = argumentos_atualizacao.parse_args()
            Missoes.atualiza_missoes(self,
            datas['id'], 
            datas['nome_missao'],
            datas['data_lancamento'],
            datas['destino'],
            datas['estado_missao'],
            datas['tripulacao'],
            datas['carga_util'],
            datas['duracao_missao'],
            datas['custo_missao'],
            datas['status_missao']
            )
            return {"message": 'Missão atualizada com sucesso!'}, 200    
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class Deleta_missao(Resource):
    def delete(self):
        try:
            datas = argumentos_exclusao.parse_args()
            Missoes.deleta_missao(self, datas['id'])
            return ({'message': 'Missão excluída com sucesso!'}), 200
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500
        
class Visualizar_missao(Resource):
    def get(self):
        try:
            missoes = Missoes.query.order_by(Missoes.id).all()
            
            missoes_json = []
            for missao in missoes:
                data_lancamento = datetime.strptime(missao.data_lancamento, '%Y-%m-%d')
                missoes_json.append({
                    'id': missao.id, 
                    'nome_missao': missao.nome_missao, 
                    'data_lancamento': data_lancamento.strftime('%Y-%m-%d'), 
                    'destino': missao.destino, 
                    'estado_missao': missao.estado_missao,
                    'tripulacao': missao.tripulacao, 
                    'carga_util': missao.carga_util, 
                    'duracao_missao': missao.duracao_missao, 
                    'custo_missao': missao.custo_missao, 
                    'status_missao': missao.status_missao
                    })

           
            return jsonify(missoes_json)
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class Visualizar_id(Resource):
    def get(self, id):
        try:
            missao = Missoes.query.get(id)

            if missao is None:
                return jsonify({"error": "Missão não encontrada"}), 404
        
            missao_json = {
                'id': missao.id,
                'nome_missao': missao.nome_missao,
                'data_lancamento': missao.data_lancamento, 
                'destino': missao.destino, 
                'estado_missao': missao.estado_missao,
                'tripulacao': missao.tripulacao, 
                'carga_util': missao.carga_util, 
                'duracao_missao': missao.duracao_missao, 
                'custo_missao': missao.custo_missao, 
                'status_missao': missao.status_missao
            }

            return jsonify(missao_json)

        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500
        
class Visualizar_data(Resource):
    def get(self):
        try:
            
            data_inicio_str = request.args.get('data_inicio')
            data_fim_str = request.args.get('data_fim')

            missoes = Missoes.query.filter(
                Missoes.data_lancamento >= data_inicio_str,
                Missoes.data_lancamento <= data_fim_str
                ).all()

            missoes_json = []
            for missao in missoes:
                missoes_json.append({
                    'id': missao.id,
                    'nome_missao': missao.nome_missao,
                    'data_lancamento': missao.data_lancamento, 
                    'destino': missao.destino, 
                    'estado_missao': missao.estado_missao,
                    'tripulacao': missao.tripulacao, 
                    'carga_util': missao.carga_util, 
                    'duracao_missao': missao.duracao_missao, 
                    'custo_missao': missao.custo_missao, 
                    'status_missao': missao.status_missao
                })

            return jsonify(missoes_json)
    
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500
