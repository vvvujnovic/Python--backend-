from fastapi import FastAPI

# Inicijalizacija FastAPI aplikacije
app = FastAPI()


# Definiranje ruta i operacija
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return {"item_id": item_id}
