import re
from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import HTTPBasicCredentials
from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr, root_validator
from bson import ObjectId
from database import collection
from security import authenticate

router = APIRouter()

class Zahtjev(BaseModel):
    korisnikEmail: EmailStr
    KategorijaUsluga: constr(min_length=1)
    vrstaCiscenja: constr(min_length=1)
    opis: constr(min_length=1)
    datum: str  # mijenjamo u običan str
    vrijeme: str  # mijenjamo u običan str

    @root_validator
    def validate_format(cls, values):
        datum = values.get("datum")
        vrijeme = values.get("vrijeme")
        datum_regex = r"\d{4}-\d{2}-\d{2}"
        vrijeme_regex = r"\d{2}:\d{2}"
        if not re.match(datum_regex, datum):
            raise ValueError("Datum nije u formatu YYYY-MM-DD")
        if not re.match(vrijeme_regex, vrijeme):
            raise ValueError("Vrijeme nije u formatu HH:MM")
        return values

class UpdateZahtjev(BaseModel):
    KategorijaUsluga: Optional[str] = None
    vrstaCiscenja: Optional[str] = None
    opis: Optional[str] = None
    datum: Optional[str] = None
    vrijeme: Optional[str] = None

@router.post("/dodaj-zahtjev")
async def dodaj_zahtjev(zahtjev: Zahtjev, credentials: HTTPBasicCredentials = Depends(authenticate)):
    try:
        # Spremi zahtjev u MongoDB
        collection.insert_one(zahtjev.dict())
        return {"message": "Zahtjev uspješno dodan!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/zahtjevi", response_model=List[Zahtjev])
async def get_zahtjevi():
    try:
        zahtjevi = list(collection.find({}, {'_id': 0}))  # Ne vraćamo '_id' polje
        return zahtjevi
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/zahtjevi/{zahtjev_id}")
async def update_zahtjev(zahtjev_id: str, zahtjev: UpdateZahtjev):
    try:
        updated_zahtjev = {k: v for k, v in zahtjev.dict().items() if v is not None}
        result = collection.update_one({"_id": ObjectId(zahtjev_id)}, {"$set": updated_zahtjev})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Zahtjev nije pronađen")
        return {"message": "Zahtjev uspješno ažuriran"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/zahtjevi/{zahtjev_id}")
async def delete_zahtjev(zahtjev_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(zahtjev_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Zahtjev nije pronađen")
        return {"message": "Zahtjev uspješno obrisan"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
