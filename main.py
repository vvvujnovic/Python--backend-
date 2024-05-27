from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from zahtjev_za_uslugom import router as zahtjev_za_uslugom_router
from ugovor_routes import router as ugovor_router
from specifikacija_usluga_routes import router as specifikacija_usluga_router


app = FastAPI()

# Omogućavanje CORS-a
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(zahtjev_za_uslugom_router)
app.include_router(ugovor_router)
app.include_router(specifikacija_usluga_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

