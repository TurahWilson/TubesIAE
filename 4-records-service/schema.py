from pydantic import BaseModel
from datetime import datetime

class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: int
    diagnosis: str

class MedicalRecordResponse(BaseModel):
    record_id: int
    patient_id: int
    doctor_id: int
    diagnosis: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PrescriptionCreate(BaseModel):
    record_id: int
    dosage: str
    instructions: str
    medicine_recipe: str

class PrescriptionResponse(BaseModel):
    prescription_id: int
    record_id: int
    dosage: str
    instructions: str
    medicine_recipe: str
    
    class Config:
        from_attributes = True