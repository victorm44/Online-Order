from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configuración de MongoDB Atlas
mongo_uri = "mongodb+srv://victor:12345@cluster.mongodb.net/order"
mongo_client = MongoClient(mongo_uri)
db = mongo_client["Order"]  # Reemplaza "nombre_base_de_datos" con el nombre de tu base de datos
clientes_collection = db["Clientes"]

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')

    cliente = clientes_collection.find_one({'usuario': usuario})

    if cliente and bcrypt.check_password_hash(cliente['contraseña'], contraseña):
        return jsonify({"message": "Autenticación exitosa"})
    else:
        return jsonify({"message": "Autenticación fallida"})

@app.route('/orden', methods=['POST'])
def crear_orden():
    data = request.get_json()
    # Realiza la lógica para crear una orden aquí
    return jsonify({"message": "Orden creada"})

if __name__ == '__main__':
    app.run(debug=True)
