from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from zahtjev_za_uslugom import router as zahtjev_za_uslugom_router

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

