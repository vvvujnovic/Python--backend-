
import pymongo  
from pymongo import MongoClient

# Uspostavljanje veze s MongoDB bazom podataka
client = MongoClient('mongodb://localhost:27017/')

# Odaberite bazu podataka
db = client['uslugebazepodataka ']

# Dobivanje kolekcije
collection = db['usluge']

# Dodavanje dokumenta
collection.insert_one({'key': 'value'})

# Preuzimanje dokumenata
documents = collection.find()

# Ispis svih dokumenata
for doc in documents:
    print(doc)
