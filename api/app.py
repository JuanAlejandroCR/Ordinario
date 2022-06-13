from flask import Flask
from flask_restful import  Api
from flask_cors import CORS
import usuarioAPI
import transaccionAPI
import resumenAPI


# Flask
app = Flask(__name__)
# Flask Restful
api = Api(app)
# Configuración del debug
app.config["DEBUG"] = True

CORS(app)

@app.route('/')
def principal():
    pag="<h1>Pagina principal</h1>"
    pag+= "<h3>Usuarios</h3>"
    pag+= "<p><a href='/users'>Para ver los usuarios ingrese aqui</a></p>"
    pag+= "<p>Si quiere ver un usuario en especifico, ingrese el email al final del enlace</p>"
    pag+= "<h3>Transacciones</h3>"
    pag+= "<p><a href='/transactions'>Para ver las transacciones ingrese aqui</a></p>"
    pag+= "<p>Si quiere ver una transaccion de un usuario en especifico, ingrese la referencia al final del enlace</p>"
    pag+= "<p><a href='summary//transactions'>Para ver las sumatorias detransacciones ingrese aqui</a></p>"
    pag+= "<p>Si quiere ver una sumatoria de transaccion de un usuario en especifico, ingrese la referencia al final del enlace</p>"
    return pag

# Añade recursos regun el endpoint
api.add_resource(usuarioAPI.Usuarios, '/users')
api.add_resource(usuarioAPI.Usuario, '/users/<user_email>')
api.add_resource(transaccionAPI.Transacciones, '/transactions')
api.add_resource(transaccionAPI.Transaccion, '/transactions/<reference>')
api.add_resource(resumenAPI.resumenUsuarios, '/summary/transactions')
api.add_resource(resumenAPI.resumenUsuario, '/summary/transactions/<user_email>')

if __name__ == "__main__":
    app.run(debug=True)    