from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

datas = []

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    age: int

class UpdateUser(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    age: int | None = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/users')
async def create_users(user: CreateUser):
    new_user_data = {
        "id": str(uuid4()),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "age": user.age
    }
    datas.append(new_user_data)
    return new_user_data
  

@app.get('/users')
async def get_users():
    return datas

@app.get('/users/{user_id}')
async def user_by_id(user_id: str):
    for user_data in datas:
        if user_data['id'] == user_id:
            return user_data
    raise HTTPException(status_code=404, detail="Data not found")

@app.patch('/users/{user_id}')
async def update_user(user: UpdateUser, user_id: str):
    for user_data in datas:
        if user_data['id'] == user_id:
            if user.first_name is not None:
                user_data['first_name'] = user.first_name
            if user.last_name is not None:
                user_data['last_name'] = user.last_name
            if user.email is not None:
                user_data['email'] = user.email
            if user.age is not None:
                user_data['age'] = user.age

            return user_data

    raise HTTPException(status_code=404, detail="Data not found")
