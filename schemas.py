from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    email: str
    age: int
    course: str

class StudentUpdate(BaseModel):
    name: str
    email: str 
    age: int 
    course: str 

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    course: str

    class Config:
        from_attributes = True