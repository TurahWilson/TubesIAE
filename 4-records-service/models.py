from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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
    
    id = Column(Integer, primary_key=True, index=True) # Changed from prescription_id to match request "id"
    patientName = Column(String, nullable=False)
    doctorName = Column(String, nullable=False)
    status = Column(String, default="pending")
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    
    items = relationship("PrescriptionItem", back_populates="prescription", cascade="all, delete-orphan")

class PrescriptionItem(Base):
    __tablename__ = "prescription_items"
    
    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"))
    medicine_id = Column(Integer, nullable=False) # Changed/Added
    medicine_name = Column(String, nullable=False) # Renamed from name
    quantity = Column(Integer, nullable=False)
    instructions = Column(String, nullable=True) # Renamed from notes
    
    prescription = relationship("Prescription", back_populates="items")

    @property
    def medicineId(self):
        return self.medicine_id

    @property
    def medicineName(self):
        return self.medicine_name