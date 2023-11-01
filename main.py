# main.py
from flask import Flask, request, jsonify
from verificadores import Autenticador, Validador, Filtro_IP, Cache

app = Flask(__name__)

# Datos para la conexión a MongoDB
url_conexion = "mongodb+srv://victor:12345@cluster0.cu54xkq.mongodb.net/?retryWrites=true&w=majority"
base_de_datos = "Order"
coleccion = "Clientes"

# Crear objetos Autenticador y Validador con los datos de conexión
validador = Validador()
autenticador = Autenticador(url_conexion, base_de_datos, coleccion)
filtro_ip = Filtro_IP()
cache = Cache()

# Establecer las relaciones
validador.establecer_siguiente(filtro_ip)
filtro_ip.establecer_siguiente(cache)
cache.establecer_siguiente(autenticador)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    datos_solicitud = request.get_json()
    
    if validador.procesar_solicitud(datos_solicitud):
        usuario = datos_solicitud.get("usuario")
        contraseña = datos_solicitud.get("contraseña")

        usuario_encontrado = autenticador.coleccion.find_one({"usuario": usuario, "contraseña": contraseña})

        if usuario_encontrado:
            if usuario_encontrado["rol"] == "admin":
                return jsonify({"mensaje": "Autenticación exitosa como administrador"})
            else:
                return jsonify({"mensaje": "Autenticación exitosa como usuario estándar"})
    
    # Autenticación fallida o validación adicional fallida
    return jsonify({"mensaje": "Autenticación fallida"})

if __name__ == '__main__':
    app.run(debug=True)
