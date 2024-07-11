from fastapi import HTTPException

from google.cloud.firestore import Client

import schema, security

def get_users(db:Client, offset: int = 0, limit: int = 100) -> list[schema.ReadUser]:
    
    user_ref = db.collection("users").offset(offset).limit(limit).stream()
    users = [{"id":user.id, **user.to_dict() }for user in user_ref]
    return users

def get_user(db:Client, id:int) -> schema.ReadUser:
    doc_ref = db.collection("users").document(id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Item not found")

def create_user(db:Client, user: schema.CreateUser) -> schema.ReadUser:
    doc_ref = db.collection("users").document()
    user_dict = user.model_dump(exclude_unset=True)
    print(user_dict)
    if 'dob' in user_dict:
        user_dict['dob'] = user.dob.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if 'password' in user_dict:
        user_dict['password'] = security.hash_password(user_dict['password'])
    if 'mobile_number' in user_dict:
        if len(user_dict['mobile_number']) != 10:
            del user_dict['mobile_number']
    doc_ref.set(user_dict)
    result = doc_ref.get().to_dict()
    return {"id": doc_ref.id, **result}


def update_user(db:Client, user_id:str, user:schema.UpdateUser) -> schema.ReadUser:
    doc_ref = db.collection("users").document(user_id)
    user_dict = user.model_dump(exclude_unset=True)
    if 'dob' in user_dict:
        user_dict['dob'] = user.dob.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if 'password' in user_dict:
        user_dict['password'] = security.hash_password(user_dict['password'])
    if 'mobile_number' in user_dict:
        if len(user_dict['mobile_number']) != 10:
            del user_dict['mobile_number']
    doc_ref.update(user_dict)
    result = doc_ref.get().to_dict()
    return {"id": doc_ref.id, **result}


def delete_user(db:Client, user_id:str) -> True:
    doc_ref = db.collection("users").document(user_id)
    doc_ref.delete()
    return True