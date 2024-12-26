from fastapi import FastAPI
#from databases import Database
import sqlite3
from crud import create_user, get_user_by_id, get_all_users, update_user, delete_user

"""Use the folowing comamnd in the terminal to activate the env"""
#env\Scripts\activate
app = FastAPI()

# SQLite database connection
DATABASE_URL = "sqlite:///./database.db"
#database = Database(DATABASE_URL)

@app.post("/users/")
def create_user_endpoint(name: str, email: str, password: str, role: str):
    return create_user(name, email, password, role)

@app.get("/users/{user_id}")
def get_user_endpoint(user_id: int):
    return get_user_by_id(user_id)

@app.get("/users/")
def get_all_users_endpoint():
    return get_all_users()

@app.put("/users/{user_id}")
def update_user_endpoint(user_id: int, name: str = None, email: str = None, role: str = None):
    return update_user(user_id, name, email, role)

@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int):
    return delete_user(user_id)


