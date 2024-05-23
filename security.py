from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "vedro"
    
    print("DEBUG: Provera autentikacije...")
    
    if credentials.username != correct_username or credentials.password != correct_password:
        print("DEBUG: Neispravni kredencijali.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neispravno korisničko ime ili lozinka",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    print("DEBUG: Autentikacija uspešna.")