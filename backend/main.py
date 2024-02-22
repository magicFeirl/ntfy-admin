from fastapi import FastAPI
from pymongo import MongoClient

from app.bili import LiveInfoCrawler

DB_URI = "mongodb+srv://ttew:114514@cluster0.l0fp2ce.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

app = FastAPI()
mongo_client = MongoClient(DB_URI)
db = mongo_client['ntfy']['ntfy']

@app.post("/add-bili")
async def add_bili(group_name, topic_name, room_id):
    doc = {
        "group_name": group_name,
        "room_id": room_id,
        "topic_name": topic_name
    }

    item = db.find_one(doc)
   
    if item:
        return {"code": 200, "message": f"group: {group_name} already has a {room_id} item"}


    LiveInfoCrawler.get_room_info(room_id)
    
    db.insert_one(doc)

    return {"code": 200, "message": "item added"}

@app.get("/list-bili")
async def list_bili():
    pass