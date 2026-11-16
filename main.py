
import os
import requests

from dotenv import load_dotenv
from pymongo import MongoClient, ReplaceOne


# 1. Charger les identifiants MongoDB
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("L'URI MongoDB est absente du fichier .env")


# 2. Connexion à MongoDB Atlas
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)

try:
    client.admin.command("ping")
    print("Connexion à MongoDB Atlas réussie !")

    db = client["Dummyjson"]


    # 3. Récupération des données depuis DummyJSON
    base_url = "https://dummyjson.com"

    endpoints = {
        "products": "produit",
        "users": "user",
        "carts": "panier"
    }

    for endpoint, collection_name in endpoints.items():

        print(f"\nRécupération des données : {endpoint}")

        response = requests.get(
            f"{base_url}/{endpoint}",
            params={"limit": 0},
            timeout=30
        )

        response.raise_for_status()

        data = response.json()
        documents = data[endpoint]

        print(f"{len(documents)} documents récupérés.")

        # 4. Préparation des documents MongoDB
        collection = db[collection_name]

        operations = []

        for document in documents:
            document["_id"] = document.pop("id")

            operations.append(
                ReplaceOne(
                    {"_id": document["_id"]},
                    document,
                    upsert=True
                )
            )

        # 5. Insertion ou mise à jour des documents
        if operations:
            collection.bulk_write(operations)

        print(
            f"Collection '{collection_name}' mise à jour : "
            f"{collection.count_documents({})} documents."
        )

    print("\nToutes les données ont été traitées avec succès !")

except Exception as error:
    print("\nUne erreur est survenue :", error)

finally:
    client.close()
