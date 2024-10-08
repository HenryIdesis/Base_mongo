from flask import Flask, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId  # Import necessário para trabalhar com ObjectId no MongoDB

load_dotenv(".cred")
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)


# Este é um exemplo simples sem grandes tratamentos de dados
@app.route('/pacientes', methods=['GET'])
def get_all_users():

    filtro = {}
    projecao = {"_id" : 0}
    dados_pacientes = mongo.db.pacientes.find(filtro, projecao)

    resp = {
        "pacientes": list( dados_pacientes )
    }

    return resp, 200


# Este é um exemplo simples sem grandes tratamentos de dados
@app.route('/pacientes', methods=['POST'])
def post_user():
    
    data = request.json

    if "cpf" not in data:
        return {"erro": "cpf é obrigatório"}, 400
    
    result = mongo.db.pacientes.insert_one(data)

    return {"id": str(result.inserted_id)}, 201

# Desafios feitos em sala, espewro que vocÊ tenha feito :)

@app.route('/pacientes/<string:id>', methods=['DELETE'])
def delete_user(id):
    try:
        # Converte a string do id para ObjectId
        filtro = {"_id": ObjectId(id)}
    except Exception as e:
        return {"erro": "ID inválido"}, 400

    print(filtro, flush=True)
    
    # Tenta encontrar e excluir o paciente com o ID fornecido
    result = mongo.db.pacientes.delete_one(filtro)

    # Verifica se um paciente foi encontrado e excluído
    if result.deleted_count == 0:
        return {"erro": "Paciente não encontrado"}, 404

    return {"mensagem": "Paciente excluído com sucesso"}, 200



if __name__ == '__main__':
    app.run(debug=True)