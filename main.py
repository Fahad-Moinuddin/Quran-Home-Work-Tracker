from fastapi import FastAPI
from databases import Database

app = FastAPI()

# SQLite database connection
DATABASE_URL = "sqlite:///./database.db"
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    query = "SELECT * FROM items"
    results = await database.fetch_all(query=query)
    return {"items": results}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str=None):
    return {"item_id": item_id, "q":q}

