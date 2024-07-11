from datetime import date
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    first_name: str
    last_name: str
    email:str|None = None
    company_name:str|None = None
    password:str|None = None
    mobile_number:str|None = None
    dob:date|None = None
    hashtag:str|None = None



class ReadUser(User):
    id:str

class CreateUser(User):
    pass

class UpdateUser(User):
    pass


class EmailSchema(BaseModel):
    email: list[EmailStr]