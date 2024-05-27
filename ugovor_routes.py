from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasicCredentials
from typing import List
from models import Ugovor, Stavka
from database import collection
from security import authenticate
from bson import ObjectId

router = APIRouter()

@router.post("/dodaj-ugovor")
async def dodaj_ugovor(ugovor: Ugovor, credentials: HTTPBasicCredentials = Depends(authenticate)):
    try:
           # Spremamo zahtjev u MongoDB
        collection.insert_one(ugovor.dict())
        return {"message": "Ugovor uspješno dodan!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ugovori", response_model=List[Ugovor])
async def get_ugovori():
    try:
        ugovori = list(collection.find({}, {'_id': 0}))  # Ne vraćamo '_id' polje
        return ugovori
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/ugovori/{ugovor_id}")
async def update_ugovor(ugovor_id: str, ugovor: Ugovor):
    try:
        updated_ugovor = {k: v for k, v in ugovor.dict().items() if v is not None}
        result = collection.update_one({"_id": ObjectId(ugovor_id)}, {"$set": updated_ugovor})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Ugovor nije pronađen")
        return {"message": "Ugovor uspješno ažuriran"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/ugovori/{ugovor_id}")
async def delete_ugovor(ugovor_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(ugovor_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Ugovor nije pronađen")
        return {"message": "Ugovor uspješno obrisan"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))