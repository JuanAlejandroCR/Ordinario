import pymongo
import json
class conection:
    def __init__(self):
        #Creando la conexion a la db y accediendo a la db
        self.client = pymongo.MongoClient("mongodb://root:ordinario@BaseDatos:27017/")
        self.database = self.client["ordinario"]
        self.users = self.database["usuarios"]
        self.transactions = self.database["transacciones"]

    def insertar_user(self, content):
        self.users.insert_one(content)

    def insertar_transaction(self,content):
        self.transactions.insert_one(content)
    
def main(cone):
    #Añadiendo usuarios por archivo
    with open ('users.json') as file:
        data = json.load(file)   
        for dato in data:
            dato['_id'] = dato.pop('user_email')
            cone.insertar_user(dato)

    #Añadiendo transacciones por archivo
    with open ('transfer.json') as file:
        data = json.load(file)
        for dato in data:
            dato['_id'] = dato.pop('reference')
            cone.insertar_transaction(dato)

if __name__ == "__main__":
    cone = conection()
    main(cone)