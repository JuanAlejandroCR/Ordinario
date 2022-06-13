import pymongo

# Conección a Mongo
conection = pymongo.MongoClient("mongodb://root:ordinario@BaseDatos:27017/")
#conection = pymongo.MongoClient("mongodb://localhost")
db =  conection["ordinario"]    # DB que se usa
collUsuarios = db["usuarios"]   # Colección que guarda a los usuarios
collTransacciones = db["transacciones"]     # Colección que guarda las transacciones

# Función que checha si un usuario existe en la DB
def usuarioEnDB(user_email):
    if collUsuarios.find_one({'_id' : user_email}) == None:
        return False    # Returna 'False' si no está
    return True     

# Función que checha si una transaccion existe en la DB
def transaccionEnDB(reference):
    if collTransacciones.find_one({'_id' : reference}) == None:
        return False
    return True 