from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kategorija_usluga import router as kategorija_usluga_router

app = FastAPI()

# Omogućavanje CORS-a
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uključivanje router-a za kategoriju usluga
app.include_router(kategorija_usluga_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

