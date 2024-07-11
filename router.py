from fastapi import APIRouter, Depends, HTTPException
from google.cloud.firestore import Client

import crud, schema, services
from db import get_db

user_router  = APIRouter()

@user_router.post("/add_users", response_model=schema.ReadUser)
def add_user(user:schema.CreateUser, db:Client = Depends(get_db)):
    user = crud.create_user(db=db, user=user)
    return user

@user_router.get("/get_users", response_model=list[schema.ReadUser])
def get_user(db:Client = Depends(get_db)):
    user = crud.get_users(db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.patch("/update_users/{user_id}", response_model=schema.ReadUser)
def update_user(user_id:str, user_data:schema.UpdateUser, db:Client = Depends(get_db)):
    user = crud.get_user(id=user_id,db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.update_user(db=db, user_id=user_id, user=user_data)
    return user

@user_router.delete("/delete_user/{user_id}")
def delete_user(user_id:str, db:Client = Depends(get_db)):
    is_deleted = crud.delete_user(db=db, id=user_id)
    if is_deleted:
        return {"message": "user deleted"}
    return {"message": "user not deleted"}

@user_router.get("/send-email")
async def send_email():
    is_success = await services.send_email()
    if is_success:
        return {"message": "email sent successfully"}
    return {"message": "Failed to send email"}