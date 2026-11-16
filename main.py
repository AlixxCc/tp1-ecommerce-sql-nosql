import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")

client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("Connexion à MongoDB Atlas réussie !")
except Exception as e:
    print("Erreur de connexion :", e)