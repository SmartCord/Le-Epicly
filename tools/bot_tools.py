from os import environ
from pymongo import MongoClient
 db_password = environ.get('db_password')
 db_uri = "mongodb://zen:{}@leepiclybot-shard-00-00-wrvha.mongodb.net:27017,leepiclybot-shard-00-01-wrvha.mongodb.net:27017,leepiclybot-shard-00-02-wrvha.mongodb.net:27017/test?ssl=true&replicaSet=LeEpiclyBot-shard-0&authSource=admin&retryWrites=true".format(db_password)

 client = MongoClient(db_uri)
 db = client['epic']
