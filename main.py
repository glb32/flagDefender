from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
app = FastAPI()
client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.mk7py.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.redditplacebot
collection = db['clients']
class Client(BaseModel):
    client_hash:str
    creation_timestamp:int
    last_used:int | None = None
    client_ip:str
    active:bool = False

@app.post("/add_client/")
async def addClient(client:Client):
    if collection.find({"client_ip":client.client_ip}):
        return {"message":"No duplicate IPs allowed"}
    elif collection.find({"client_hash":client.client_hash}):
        return {"message":"Client already exists"}
    else:
        collection.insert_one(client.__dict__)
        return {"message":"Client {client.client_id} added"}

@app.get("/get_client/{client_hash}")
async def getClient(client_hash:str, client_ip:str):
    if collection.find_one({"client_hash":client_hash,"client_ip":client_ip}) is not None: 
        return {"message":f"Client {client_hash} found"}
    else:
        return {"message":f"Client {client_hash} not found"}