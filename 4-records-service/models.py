from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    
    record_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    diagnosis = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Prescription(Base):
    __tablename__ = "prescriptions"
    
    prescription_id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, nullable=False)
    dosage = Column(String, nullable=False)
    instructions = Column(String, nullable=False)
    medicine_recipe = Column(String, nullable=False)