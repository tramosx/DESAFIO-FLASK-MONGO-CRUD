from flask import Flask, request, jsonify
from bson import ObjectId
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb://localhost:27017/new_database'

mongo = PyMongo(app)
db = mongo.db
    
@app.route('/noticias')
def noticias():
    _noticias = db.noticia.find()

    item_noticia = {}
    data = []
    for noticia in _noticias:
        item_noticia = {
            'id': str(noticia['_id']),
            'titulo': noticia['titulo'],
            'texto': noticia['texto'],
            'autor': db.autor.find_one({"_id" : noticia['autor']},)["nome"]
        }
        data.append(item_noticia)

    return jsonify(data=data)
    
    
@app.route('/cadastrar_noticia', methods=['POST'])
def cadastrar_noticia():
    data = request.get_json(force=True)
    
    _verifica_autor = db.autor.find_one({"nome" : data['autor']},)
    
    if _verifica_autor:
        id_autor = _verifica_autor['_id']
    else:
        id_autor = db.autor.insert_one({"nome" : data['autor'] })
        id_autor = id_autor.inserted_id
    
    item_noticia = {
        'titulo': data['titulo'],
        'texto': data['texto'],
        'autor': id_autor
    }
    db.noticia.insert_one(item_noticia)

    return jsonify(message='To-do saved successfully!'), 201


@app.route('/pesquisar_noticia', methods=['POST'])
def pesquisar_noticia():
    data = request.get_json(force=True)
    item_noticia = {}

    if data.get("titulo"):
        key = "titulo"
        valor = data.get("titulo")
    else:
        if data.get("texto"):
            key = "texto"
            valor = data.get("texto")
        else:    
            if data.get("autor"):
                key = "autor"
                valor = data.get("autor")
            else:
                key = None
                valor = None  
                
    if key == "autor":       
        _verifica_autor = db.autor.find_one({"nome" : valor},)
        if _verifica_autor:
            valor = _verifica_autor['_id']
        else:
            valor = None
                
                
    _pequisa_noticia = db.noticia.find({key : valor})
    
    dados = []            

    for noticia in _pequisa_noticia:
        item_noticia = {
            'id': str(noticia['_id']),
            'titulo': noticia['titulo'],
            'texto': noticia['texto'],
            'autor': db.autor.find_one({"_id" : noticia['autor']},)["nome"]
        }
        dados.append(item_noticia)

    
    return jsonify(dados=dados)


@app.route('/visualizar_noticia', methods=['POST'])
def visualizar_noticia():
    data = request.get_json(force=True)
    item_noticia = {}

    titulo = None
    texto = None
    autor = None


    if data.get("titulo"):
        titulo = data.get("titulo")
    if data.get("texto"):
        texto = data.get("texto")
    if data.get("autor"):
        autor = data.get("autor")
        
    if autor:
        _verifica_autor = db.autor.find_one({"nome" : autor},)
        if _verifica_autor:
            valor = _verifica_autor['_id']
        else:
            valor = None
                
    _visualiza_noticia = db.noticia.find({"titulo" : titulo, "texto" : texto, "autor": valor})
    
    dados = []            

    for noticia in _visualiza_noticia:
        
        item_noticia = {
            'id': str(noticia['_id']),
            'titulo': noticia['titulo'],
            'texto': noticia['texto'],
            'autor': db.autor.find_one({"_id" : noticia['autor']},)["nome"]
        }
        dados.append(item_noticia)

    
    return jsonify(dados=dados)


@app.route('/editar_noticia', methods=['PUT'])
def editar_noticia():
    data = request.get_json(force=True)
    item_noticia = {}

    id = None
    titulo = None
    texto = None
    autor = None

    if data.get("id"):
        id = data.get("id")
 
    if data.get("autor"):
        autor = data.get("autor")
        
    if autor:
        _verifica_autor = db.autor.find_one({"nome" : autor},)
        if _verifica_autor:
            valor = _verifica_autor['_id']
        else:
            valor = None
                
                
    _visualiza_noticia = db.noticia.find_one({'_id': ObjectId(id)})
    
    if _visualiza_noticia:
        
        if data.get("titulo"):
            titulo = data.get("titulo")
        else:
            titulo = _visualiza_noticia['titulo']
            
        if data.get("texto"):
            texto = data.get("texto")
        else:
            texto = _visualiza_noticia['texto']
            
        if data.get("autor"):
            autor = data.get("autor")
        else:
            autor = _visualiza_noticia['autor']
        
        db.noticia.update({'_id' : ObjectId(id)}, {"$set": {"titulo": titulo, "texto" : texto, "autor" : autor}})
        
        return jsonify(dados=["Dados atualizados com sucesso!!"])
    else:
        return jsonify(dados=["ID não existe"])
        
@app.route('/deletar_noticia/<id>', methods=['DELETE'])
def deletar_noticia(id):
    db.noticia.remove({"_id" : ObjectId(id)})
    return jsonify(data=["Noticia removida com sucesso"])

@app.route('/autores')
def autores():
    _autores = db.autor.find()

    item_autor = {}
    data = []
    for autor in _autores:
        item_autor = {
            'id': str(autor['_id']),
            'nome': autor['nome']
        }
        data.append(item_autor)

    return jsonify(data=data)


if __name__ == '__main__':
    app.run(debug=True)
