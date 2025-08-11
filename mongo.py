from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    # Подключение к MongoDB (стандартные параметры)
    client = MongoClient("mongodb://localhost:27017/")
    
    # Проверка подключения
    client.admin.command('ping')
    print("Успешное подключение к MongoDB!")
    

except ConnectionFailure as e:
    print(f"Ошибка подключения: {e}")
finally:
    client.close()