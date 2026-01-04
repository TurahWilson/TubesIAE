from pydantic import BaseModel, EmailStr

class PatientCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    gender: str
    address: str

class PatientResponse(BaseModel):
    patient_id: int
    name: str
    email: str
    phone_number: str
    gender: str
    address: str
    
    class Config:
        from_attributes = True