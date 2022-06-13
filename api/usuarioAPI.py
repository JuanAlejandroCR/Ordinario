from flask import jsonify, request
from flask_restful import Resource
from coneccionDB import collUsuarios, usuarioEnDB

# Clase pa' el endpoint '/users'
class Usuarios(Resource):
    def get(self):        # Función pa' el método GET
        lstUsuarios = [usuario for usuario in collUsuarios.find()]      # Genera una lista de los usuarios existentes
        if (len(lstUsuarios) > 0): 
            for usuario in lstUsuarios:
                usuario['user_email'] = usuario.pop('_id')
            return jsonify(lstUsuarios)     # Retorna la lista
        else:
            response = jsonify({"msg" : "No hay usuarios la db"})       # En caso de que no existan usuario
            response.status_code = 404
            return response 

    def post(self):     # Función para el método POST
        usuario = {     # Crea un diccionario con el request
        '_id' : request.json['user_email'],
        'first_name' : request.json['first_name'],
        'last_name' : request.json['last_name'],
        'address' : request.json['address'],
        }
    
        if usuarioEnDB(usuario['_id']) == False:    # Checa si el usuario existe
            collUsuarios.insert_one(usuario)        # Lo inserta
            usuario['user_email'] = usuario.pop('_id')      # Cambia la key 
            return jsonify({"msg": "Usuario creado" ,"usuario" : usuario})
        else: 
            response = jsonify({"msg" : "Usuario existente en la db"})
            response.status_code = 404
            return response

# Clase pa' el endpoint '/users/{user_email}'
class Usuario(Resource):   
    def get(self,user_email):       # Función para el método GET
        usuario = collUsuarios.find_one({'_id' : user_email})       # Busca un usuario con el 'user_email' indicado
        if usuarioEnDB(user_email) == False:  
            response = jsonify({"msg" : "Usuario no existe en la db"})
            response.status_code = 404
            return response      
        else:        
            usuarioEmail = {}        
            usuarioEmail['user_email'] = usuario['_id']

            for key,value in usuario.items():
                    if key == '_id':                
                        continue
                    usuarioEmail[key] = value

            return jsonify(usuarioEmail)        # Retorna el usuario

    def delete(self,user_email):        # Función para el método DELETE
        if usuarioEnDB(user_email) == False:                    
            response = jsonify({"msg" : "Usuario no existe en la db"})
            response.status_code = 404
            return response   
        else: 
            collUsuarios.delete_one({'_id': user_email})    # Borra al usuario
            return jsonify({'msg': 'Usuario eliminado'})

    def put(self,user_email):       # Función para el método PUT
        #usuario = collUsuarios.find_one({'_id' : user_email})
        if usuarioEnDB(user_email) == False:        
            response = jsonify({"msg" : "Usuario no existe en la db"})
            response.status_code = 404
            return response   
        else: 
            usuario = {
                '_id' : request.json['user_email'],
                'first_name' : request.json['first_name'],
                'last_name' : request.json['last_name'],
                'address' : request.json['address'],
            }
            
            collUsuarios.update_one({'_id':user_email},     # Actualiza al usuario
            {'$set': usuario})
            return jsonify({'msg': 'Usuario actualizado'})            