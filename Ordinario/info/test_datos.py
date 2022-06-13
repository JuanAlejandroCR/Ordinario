import unittest
import json
from os import path
import pymongo
from datos import conection

class testApi(unittest.TestCase):
    def setUp(self):                    
        self.appDB = conection()      # Objeto de tipo app, que nos ayudará a conectarnos a la DB

    # Verifica atributos del objeto
    def test_appDB(self):
        client = pymongo.MongoClient("mongodb://root:ordinario@BaseDatos:27017/")
        db = client['ordinario']
        self.assertEqual(self.appDB.client,client, "Obtenido(%s) deberia ser %s" % (self.appDB.client,client))
        self.assertEqual(self.appDB.database,db, "Obtenido(%s) deberia ser %s" % (self.appDB.database,db))

    #Se comprueba la funcion insertar_transaccion
    def test_insertar_transaccion(self):
        content = {
                    "_id": "000070",
                    "date": "2020-01-10",
                    "amount": "-150.72",
                    "type": "outflow",
                    "category": "transfer",
                    "user_email": "jaime@email.com"
                }
        
        self.appDB.insertar_transaction(content)

        consulta = self.appDB.transactions.find_one({'_id' : "000070"})        
        consultaDicc = {
                '_id': consulta['_id'],
                'date': consulta['date'],
                'amount': consulta['amount'],
                'type': consulta['type'],
                'category': consulta['category'],
                'user_email' : consulta['user_email']
            }   
        
        self.assertEqual(consultaDicc, content, "Obtenido(%s) deberia ser %s" % (consultaDicc, content))

    #Se comprueba la funcion insertar_user
    def test_insertar(self):
        content = {
                    "first_name": "Jaime",
                    "last_name": "Mausan",
                    "address": "Tepic #4301",
                    "_id": "Jaime@email.com"
                }

        self.appDB.insertar_user(content)        

        consulta = self.appDB.users.find_one({"_id": "Jaime@emailc.com"})
        consultaDicc = {
                'first_name': consulta['first_name'],
                'last_name': consulta['last_name'],
                'address' : consulta['address'],
                '_id': consulta['_id']
            }   
        
        self.assertEqual(consultaDicc, content, "Obtenido(%s) deberia ser %s" % (consultaDicc, content)) 


if __name__ == '__main__':    
    unittest.main()