from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional

class Zahtjev(BaseModel):
    korisnikEmail: EmailStr
    KategorijaUsluga: constr(min_length=1)
    vrstaCiscenja: constr(min_length=1)
    opis: constr(min_length=1)
    datum: str
    vrijeme: str
    komentar: Optional[str] = None  

class Usluga(BaseModel):
    naziv_usluge: str
    cijena_usluge: float
    opis: Optional[str] = None

class Stavka(BaseModel):
    naziv_uslug: str
    kolicina: int
    cijena_usluge: float
    datum_dostupnosti_usluge: str


class Ugovor(BaseModel):
    korisnikEmail: EmailStr
    datum_ugovora: str
    stavke: List[Stavka]
    ukupna_cijena: float
