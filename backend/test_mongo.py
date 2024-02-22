from datetime import datetime
from pymongo import MongoClient

import os

uri = "mongodb+srv://ttew:114514@cluster0.l0fp2ce.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri)

db = client['user']
collection = db['info']

user_info = {
    "name": "idk",
    "age": 112,
    "reg_at": datetime.now()
}

print(collection.insert_one(user_info).inserted_id)