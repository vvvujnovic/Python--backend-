from pymongo import MongoClient

def connect_to_mongodb():
    uri = "mongodb://localhost:27017/"

    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        return None

client = connect_to_mongodb()

if client:
    # Odaberite bazu podataka
    db = client['uslugebazepodataka']
    # Naziv kolekcija
    zahtjevi_collection = db['zahtjevi_za_uslugom']
    usluge_collection = db['usluge']
    ugovor_collection = db['ugovori']  
  

else:
    collection = None
    ugovor_collection = None
    usluga_collection = None









