from app import db

class Missoes(db.Model):
    __tablename__ = 'missoes'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True) 
    nome_missao = db.Column(db.String(100), nullable=True, unique=True)
    data_lancamento = db.Column(db.String(50), nullable=False)
    destino = db.Column(db.String(150), nullable=False)
    estado_missao = db.Column(db.String(30), nullable=False)
    tripulacao = db.Column(db.String(300), nullable=False)  
    carga_util = db.Column(db.String(300), nullable=False)
    duracao_missao = db.Column(db.String(100), nullable=False)  
    custo_missao = db.Column(db.Float, nullable=False)
    status_missao = db.Column(db.String(100), nullable=False)


    def __init__(self, nome_missao, data_lancamento, destino, estado_missao, tripulacao, carga_util, duracao_missao, custo_missao, status_missao):
        self.nome_missao = nome_missao
        self.data_lancamento = data_lancamento
        self.destino = destino
        self.estado_missao = estado_missao
        self.tripulacao = tripulacao
        self.carga_util = carga_util
        self.duracao_missao = duracao_missao
        self.custo_missao = custo_missao
        self.status_missao = status_missao

    def salva_missao(self, nome_missao, data_lancamento, destino, estado_missao, tripulacao, carga_util, duracao_missao, custo_missao, status_missao):
        try:
            add_banco = Missoes(nome_missao, data_lancamento, destino, estado_missao, tripulacao, carga_util, duracao_missao, custo_missao, status_missao)
            print(add_banco)
            db.session.add(add_banco)
            db.session.commit()
        except Exception as e:
            print(e)

    def atualiza_missoes(self,id, nome_missao, data_lancamento, destino, estado_missao, tripulacao, carga_util, duracao_missao, custo_missao, status_missao):
        try:
            db.session.query(Missoes).filter(Missoes.id==id).update({"nome_missao":nome_missao,"data_lancamento":data_lancamento,"destino":destino,"estado_missao":estado_missao,"tripulacao":tripulacao,"carga_util":carga_util,"duracao_missao":duracao_missao,"custo_missao":custo_missao,"status_missao":status_missao})
            db.session.commit()
        except Exception as e:
            print(f"Erro ao recuperar todas as missões: {e}")

    def deleta_missao(self, id):
        try:
            db.session.query(Missoes).filter(Missoes.id==id).delete()
            db.session.commit()
        except Exception as e:
            print(e)