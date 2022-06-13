from flask import jsonify, request
from flask_restful import Resource
from coneccionDB import transaccionEnDB , usuarioEnDB, collTransacciones, collUsuarios

# Clase pa' el endpoint '/summary/transactions'
class resumenUsuarios(Resource):
    def __init__(self) -> None:        
        # Genera una lista de los 'user_email' de todos los usuarios que tengan alguna transacción
        self.usuariosEmailLst = list(set([transaccion['user_email'] for transaccion in collTransacciones.find()]))
        # Genera una lista de todas las transacciones existentes
        self.transaccionesLst = [transaccion for transaccion in collTransacciones.find()]

    def get(self):  # Función para el método GET
        lstResumen = []     # Lista que guarda los resumenes
        total_inflow = 0
        total_outflow = 0

        if (len(self.transaccionesLst) == 0):   # Checa si hay transacciones en la db
            response = jsonify({"msg" : "No hay transacciones en la db"})
            response.status_code = 404
            return response 
        else:
            for usuarioEmail in self.usuariosEmailLst:      # Itera en la lista de emails
                data = {}       # Diccionario pa' el resumen del usuario
                data['user_email'] = usuarioEmail
                for transaccion in self.transaccionesLst:   # Itera en la lista de las transacciones
                    if transaccion['user_email'] == usuarioEmail:   # Checa si la transacción le corresponde a 'usuarioEmail'
                        if transaccion['type'] == "inflow":     # Verifica el tipo de transacción
                            total_inflow += float(transaccion['amount'])    #     Lo suma
                        else :                                              #   a su respectivo
                            total_outflow += float(transaccion['amount'])   #      tipo
                
                data['total_inflow'] = str(round(total_inflow,2))       #   Cambia el tipo
                data['total_outflow'] = str(round(total_outflow,2))     #     a string
                lstResumen.append(data)     # Añade el diccionario a la lista
                total_inflow = 0 ; total_outflow = 0    # Resetea los totales

            return jsonify(lstResumen)      # Retorna la lista

# Clase pa' el endpoint '/summary/transactions/<user_email>'
class resumenUsuario(Resource):
    def __init__(self) -> None:        
        self.usuariosEmailLst = list(set([transaccion['user_email'] for transaccion in collTransacciones.find()]))

    def get(self,user_email):       # Función para el método GET
        if usuarioEnDB(user_email) == False:    # Checa si el usuario está en la db
            response = jsonify({"msg" : "Usuario no existe en la db"})
            response.status_code = 404
            return response
        if self.usuariosEmailLst.count(user_email) == 0:    # Checa si el usuario tiene transacciones 
            response = jsonify({"msg" : "Usuario no tiene transacciones"})
            response.status_code = 404
            return response

        # Genera una lista de todas las transacciones correspondientes pa' el usuario 
        transaccionesLst = [transaccion for transaccion in collTransacciones.find() if transaccion['user_email']==user_email]        
        # Diccionario pa' el resumen del usuario
        data = {
            'inflow' : {},
            'outflow' : {}
        }
        inflow = {}
        outflow = {}

        for transaccion in transaccionesLst:    # Itera en la lista de transacciones
            if transaccion['type'] == 'inflow':     # Checa el tipo 
                if inflow.get(transaccion['category']) != None:     # Checa si inflow ya tiene una key con el nombre del actual category
                    valorActual = float(inflow[transaccion['category']])    
                    suma = valorActual + float(transaccion['amount'])       # En caso se que si, hace una sumatorio
                    inflow[transaccion['category']] = str(suma)     # Asigna valor a la key y además lo convierte a String
                else:
                    inflow[transaccion['category']] = transaccion['amount']
            else:
                if outflow.get(transaccion['category']) != None:
                    valorActual = float(outflow[transaccion['category']])
                    suma = valorActual + float(transaccion['amount'])
                    outflow[transaccion['category']] = str(suma)
                else:
                    outflow[transaccion['category']] = transaccion['amount']

        data['inflow'] = inflow     # Añade valor a las key
        data['outflow'] = outflow
        return jsonify(data)       # Retorna el diccionario que contiene el resumen