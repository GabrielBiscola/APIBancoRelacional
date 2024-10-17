import json
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask('carros')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/bd_carro'

mybd = SQLAlchemy(app)

class Carros(mybd.Model):
    __tablename__ = 'tb_carros'
    id = mybd.Column(mybd.Integer(), primary_key = True)
    marca = mybd.Column(mybd.String(50))
    nome = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float)
    cor = mybd.Column(mybd.String(50))
    numero_vendas = mybd.Column(mybd.Float())
    ano = mybd.Column(mybd.Integer())

    def to_json(self):
        return{"id":self.id,"marca":self.marca,"nome":self.nome, "valor":self.valor ,"cor":self.cor,"numero_vendas":self.numero_vendas,"ano":self.ano}

@app.route("/carros", methods=["GET"])
def selecionar_carros():
    carro_objetos = Carros.query.all()

    carro_json = [carro.to_json() for carro in carro_objetos]

    return gera_response(200, "carros", carro_json)

@app.route("/carros/<id_p>", methods=["GET"])
def seleciona_carro_id(id_p):
    carro_objetos = Carros.query.filter_by(id=id_p).first()
    carro_json = carro_objetos.to_json()

    return gera_response(200, "carros", carro_json)

@app.route("/carros", methods=["POST"])
def criar_carro():
    body = request.get_json()

    try:
        carro = Carros(id=body["id"], marca=body["marca"], nome=body["nome"], valor=body["valor"], cor=body["cor"], numero_vendas=body["numero_vendas"], ano=body["ano"])
        
        mybd.session.add(carro)
        mybd.session.commit()

        return gera_response(201, "carros", carro.to_json(), "Criado com Sucesso!")
    
    except Exception as e:
        print("Erro", e)

        return gera_response(400, "carros", {}, "Erro ao cadastrar")
    
@app.route("/carros/<id>", methods=["PUT"])

def atualizar_carro(id):
    carro_objetos = Carros.query.filter_by(id=id).first()
    body = request.get_json()
    
    try:
        if('marca' in body):
            carro_objetos.marca = body['marca']
        if('nome' in body):
            carro_objetos.nome = body['nome']
        if('valor' in body):
            carro_objetos.valor = body['valor']
        if('cor' in body):
            carro_objetos.cor = body['cor']
        if('numero_vendas' in body):
            carro_objetos.numero_vendas = body['numero_vendas']
        if('ano' in body):
            carro_objetos.ano = body['ano'] 

        mybd.session.add(carro_objetos)
        mybd.session.commit()

        return gera_response(200, "carros", carro_objetos.to_json(), "Atualizado com sucesso")

    except Exception as e:
         print('Erro', e)
         return gera_response(400, "carros", {}, "Erro ao atualizar")
    
@app.route("/carros/<id>", methods=["DELETE"])
def deletar_carro(id):
    carro_objetos = Carros.query.filter_by(id=id).first()
    
    try:
        mybd.session.delete(carro_objetos)
        mybd.session.commit()
        return gera_response(200, "carros", carro_objetos.to_json(), "Deletado com sucesso")
    
    except Exception as e:
        print("Erro", e)
        return gera_response(400, "carro", {}, "Erro ao deletar")

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo
    
    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

app.run(port=5000, host='localhost', debug=True)