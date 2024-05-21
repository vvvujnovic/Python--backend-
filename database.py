from pymongo import MongoClient

def connect_to_mongodb():
    # URI za povezivanje s lokalnim MongoDB poslužiteljem
    uri = "mongodb://localhost:27017/"

    try:
        # Povezivanje s MongoDB poslužiteljem
        client = MongoClient(uri)
        
        # Provjera uspješne veze slanjem pinga
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        return client
    except Exception as e:
        print(e)
        return None

# Uspostavljanje veze s MongoDB bazom podataka
client = connect_to_mongodb()

if client:
    # Odaberite bazu podataka
    db = client['uslugebazepodataka']

    # Dobivanje kolekcije
    collection = db['usluge']

    # Dodavanje dokumenta
    collection.insert_one({'key': 'value'})

    # Preuzimanje dokumenata
    documents = collection.find()

    # Ispis svih dokumenata
    for doc in documents:
        print(doc)







