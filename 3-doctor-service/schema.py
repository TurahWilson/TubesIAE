from pydantic import BaseModel, EmailStr

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    phone_number: str
    email: EmailStr
    license_number: str

class DoctorResponse(BaseModel):
    doctor_id: int
    name: str
    specialization: str
    phone_number: str
    email: str
    license_number: str
    
    class Config:
        from_attributes = True