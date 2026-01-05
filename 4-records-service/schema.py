from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Medical Record Schemas (Existing) ---
class MedicalRecordBase(BaseModel):
    patient_id: int
    doctor_id: int
    diagnosis: str

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordResponse(MedicalRecordBase):
    record_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# --- Prescription Schemas (New) ---
class PrescriptionItemBase(BaseModel):
    medicineId: int
    medicineName: str
    quantity: int
    instructions: Optional[str] = None

class PrescriptionItemResponse(PrescriptionItemBase):
    pass
    class Config:
        orm_mode = True

class PrescriptionCreate(BaseModel):
    patientName: str
    doctorName: str
    status: str = "pending"
    items: List[PrescriptionItemBase]

class PrescriptionUpdate(BaseModel):
    patientName: Optional[str] = None
    doctorName: Optional[str] = None
    status: Optional[str] = None
    items: Optional[List[PrescriptionItemBase]] = None

class PrescriptionResponse(BaseModel):
    id: int
    patientName: str
    doctorName: str
    status: str
    createdAt: datetime
    items: List[PrescriptionItemResponse]
    
    class Config:
        orm_mode = True