from flask import jsonify, request
from flask_restful import Resource
from coneccionDB import transaccionEnDB , usuarioEnDB, collTransacciones

# Función que verifica que los valores del request sean adecuados a las reglas específicadas pa' el proyecto
def validarTransaccion(transaccion):    
    if not(transaccion['type'] == 'inflow' or transaccion['type'] == 'outflow'):    # Si el tipo de transacción no es válido
        response = jsonify({"msg" : "Tipo de transaccion no valido"})
        return response 
    if transaccion['type'] == "inflow":     # Si la cantidad sea acertada al tipo
        if float(transaccion['amount']) < 0:
            response = jsonify({"msg" : "La cantidad debe de ser positiva"})
            return response 
    else:
         if float(transaccion['amount']) > 0:
            response = jsonify({"msg" : "La cantidad debe de ser negativa"})
            return response  
    return True         # Returna True en caso de que la transacción sea válida

# Clase pa' el endpoint '/transactions'
class Transacciones(Resource):
    def get(self):      # Función para el método GET
        # Genera una lista de las transacciones
        lstTransacciones = [transaccion for transaccion in collTransacciones.find()]
        
        if (len(lstTransacciones) > 0): 
            for transaccion in lstTransacciones:
                transaccion['reference'] = transaccion.pop('_id')
            return jsonify(lstTransacciones)
        else:
            response = jsonify({"msg" : "No hay transacciones en la db"})
            response.status_code = 404
            return response 


    def post(self):      # Función para el método POST
        # Genera un diccionario segun el request
        transaccion = {
        '_id' : request.json['reference'],
        'date' : request.json['date'],
        'amount' : request.json['amount'],
        'type' : request.json['type'],
        'category' : request.json['category'],
        'user_email' : request.json['user_email'],
        }
    
        if usuarioEnDB(transaccion['user_email']) == False:     # Verifica si el usuario existe en la db
            response = jsonify({"msg" : "Usuario no existe en la db"})
            response.status_code = 404
            return response

        if transaccionEnDB(transaccion['_id']) == True:     # Verifica si la transacción existe en la db
            response = jsonify({"msg" : "Transaccion existente en la db"})
            response.status_code = 404
            return response

        validar = validarTransaccion(transaccion)       # Llama a la función validarTransaccion
        if validar != True:
            return validar
    
        collTransacciones.insert_one(transaccion)       # Inserta la transacción a la db
        transaccion['reference'] = transaccion.pop('_id')       # Cambia la key
        return jsonify({"msg": "Transaccion creada" ,"transaccion" : transaccion})      # Returna un msg al igual que la transacción ing
        resada

# Clase pa' el endpoint '/transactions/<reference>'
class Transaccion(Resource):   
    def get(self,reference):     # Función para el método GET
        transaccion = collTransacciones.find_one({'_id' : reference})       # Obtiene la trasacción
        if transaccionEnDB(reference) == False:  
            response = jsonify({"msg" : "Transaccion no existe en la db"})
            response.status_code = 404
            return response      
        else:   
            transaccion['reference'] = transaccion.pop('_id')     
            return jsonify(transaccion)

    def delete(self,reference):     # Función para el método DELETE
        if transaccionEnDB(reference) == False:         # Verifica si existe la transacción
            response = jsonify({"msg" : "Transaccion no existe en la db"})
            response.status_code = 404
            return response   
        else: 
            collTransacciones.delete_one({'_id': reference})    # Borra la transacción
            return jsonify({'msg': 'Transaccion eliminada'})

    def put(self,reference):        # Función para el método PUT
        #transaccion = collTransacciones.find_one({'_id' : reference})
        if transaccionEnDB(reference) == False:  
            response = jsonify({"msg" : "Transaccion no existe en la db"})
            response.status_code = 404
            return response   
        else: 
            transaccion = {
                '_id' : request.json['reference'],
                'date' : request.json['date'],
                'amount' : request.json['amount'],
                'type' : request.json['type'],
                'category' : request.json['category'],
                'user_email' : request.json['user_email'],
            }
            validar = validarTransaccion(transaccion)       # Valida la transacción
            if validar != True:
                return validar
            
            collTransacciones.update_one({'_id':reference},     # Actualiza la transacción
            {'$set': transaccion})
            return jsonify({'msg': 'Transaccion actualizada'})            