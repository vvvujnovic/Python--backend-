import re
from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import HTTPBasicCredentials
from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr, validator
from bson import ObjectId
from database import zahtjevi_collection 
from security import authenticate
from models import Zahtjev, UpdateZahtjev

router = APIRouter()

@router.post("/dodaj-zahtjev")
async def dodaj_zahtjev(zahtjev: Zahtjev, credentials: HTTPBasicCredentials = Depends(authenticate)):
    try:
          # Spremamo zahtjev u novu kolekciju zahtjevi_collection
        zahtjevi_collection.insert_one(zahtjev.dict())
        return {"message": "Zahtjev uspješno dodan!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/zahtjevi", response_model=List[Zahtjev])
async def get_zahtjevi():
    try:
        zahtjevi = list(zahtjevi_collection.find({}, {'_id': 0}))  # Ne vraćamo '_id' polje
        return zahtjevi
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/zahtjevi/{korisnikEmail}", response_model=List[Zahtjev])
async def get_zahtjevi_po_emailu(korisnikEmail: str):
    try:
        zahtjevi = list(zahtjevi_collection.find({"korisnikEmail": korisnikEmail}, {'_id': 0}))
        if not zahtjevi:
            raise HTTPException(status_code=404, detail="Zahtjevi nisu pronađeni")
        return zahtjevi
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/zahtjevi/{zahtjev_id}")
async def update_zahtjev(zahtjev_id: str, zahtjev: UpdateZahtjev, komentar: Optional[str] = None):
    try:
        # Ažurirajte komentar ako je poslan
        if komentar:
            updated_zahtjev = zahtjev.dict()
            updated_zahtjev["komentar"] = komentar
        else:
            updated_zahtjev = {k: v for k, v in zahtjev.dict().items() if v is not None}
        result = zahtjevi_collection.update_one({"_id": ObjectId(zahtjev_id)}, {"$set": updated_zahtjev})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Zahtjev nije pronađen")
        return {"message": "Zahtjev uspješno ažuriran"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/zahtjevi/{zahtjev_id}")
async def delete_zahtjev(zahtjev_id: str):
    try:
        result = zahtjevi_collection.delete_one({"_id": ObjectId(zahtjev_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Zahtjev nije pronađen")
        return {"message": "Zahtjev uspješno obrisan"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







