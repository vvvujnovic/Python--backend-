from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import HTTPBasicCredentials
from typing import List, Optional
from models import Usluga
from database import collection  
from security import authenticate

router = APIRouter()

@router.post("/dodaj-uslugu")
async def dodaj_uslugu(usluga: Usluga, credentials: HTTPBasicCredentials = Depends(authenticate)):
    try:
        collection.insert_one(usluga.dict())
        return {"message": "Usluga uspješno dodana!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usluge", response_model=List[Usluga])
async def get_usluge():
    try:
        usluge = list(collection.find({}, {'_id': 0}))  # Ne vraćamo '_id' polje
        return usluge
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/usluge/{usluga_id}")
async def update_uslugu(usluga_id: str, usluga: Usluga):
    try:
        updated_usluga = {k: v for k, v in usluga.dict().items() if v is not None}
        result = collection.update_one({"_id": ObjectId(usluga_id)}, {"$set": updated_usluga})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Usluga nije pronađena")
        return {"message": "Usluga uspješno ažurirana"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/usluge/{usluga_id}")
async def delete_uslugu(usluga_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(usluga_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Usluga nije pronađena")
        return {"message": "Usluga uspješno obrisana"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
