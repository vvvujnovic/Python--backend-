from pydantic import BaseModel, EmailStr, constr, validator
from typing import List, Optional
from datetime import datetime
import re

class Zahtjev(BaseModel):
    korisnikEmail: EmailStr
    KategorijaUsluga: constr(min_length=1)
    vrstaCiscenja: constr(min_length=1)
    opis: constr(min_length=1)
    datum: datetime
    vrijeme: str
    komentar: Optional[str] = None  

@validator("datum", pre=True)
def parse_datum(cls, value):
        return datetime.strptime(value, "%Y-%m-%d")

@validator("vrijeme")
def validate_vrijeme(cls, v):
        if not re.match(r"\d{2}:\d{2}", v):
            raise ValueError("Vrijeme nije u formatu HH:MM")
        return v


class Usluga(BaseModel):
    naziv_usluge: str
    cijena_usluge: float
    valuta: str = "EUR"
    opis: Optional[str] = None

    @validator("cijena_usluge")
    def validate_cijena(cls, v):
        if v <= 0:
            raise ValueError("Cijena usluge mora biti veća od 0")
        return v

    @validator("naziv_usluge")
    def validate_naziv_usluge(cls, v):
        if len(v.strip()) == 0:
            raise ValueError("Naziv usluge ne može biti prazan")
        return v

class Stavka(BaseModel):
    naziv_usluge: str
    kolicina: int
    cijena_usluge: float
    valuta: str = "EUR"
    datum_dostupnosti_usluge: datetime

@validator("datum_dostupnosti_usluge", pre=True)
def parse_datum_dostupnosti_usluge(cls, value):
        return datetime.strptime(value, "%Y-%m-%d")



class Ugovor(BaseModel):
    ime_prezime: str
    broj_narudžbe: int
    naziv_servisa: str
    datum_ugovora: datetime
    stavke: List[Stavka]
    ukupna_cijena: float
    valuta: str = "EUR"

@validator("datum_ugovora", pre=True)
def parse_datum_ugovora(cls, value):
        return datetime.strptime(value, "%Y-%m-%d")


class UpdateZahtjev(BaseModel):
    KategorijaUsluga: Optional[str] = None
    vrstaCiscenja: Optional[str] = None
    opis: Optional[str] = None
    datum: Optional[str] = None
    vrijeme: Optional[str] = None

@validator("datum", pre=True)
def parse_datum(cls, value):
        if value is not None:
            return datetime.strptime(value, "%Y-%m-%d")
        return value

@validator("vrijeme")
def validate_vrijeme(cls, v):
        if v is not None and not re.match(r"\d{2}:\d{2}", v):
            raise ValueError("Vrijeme nije u formatu HH:MM")
        return v


