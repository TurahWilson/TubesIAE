from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import models, database, schema
from database import engine, get_db
import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Records Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTH_SERVICE_URL = "http://localhost:8001"

def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization header")
    
    try:
        token = authorization.split(" ")[1]
        response = requests.post(
            f"{AUTH_SERVICE_URL}/verify-token",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def read_root():
    return {"service": "Records Service", "status": "running"}

# ============= MEDICAL RECORDS ENDPOINTS =============

@app.get("/records", response_model=List[schema.MedicalRecordResponse])
def get_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    records = db.query(models.MedicalRecord).offset(skip).limit(limit).all()
    return records

@app.get("/records/{record_id}", response_model=schema.MedicalRecordResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    record = db.query(models.MedicalRecord).filter(models.MedicalRecord.record_id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record

@app.post("/records", response_model=schema.MedicalRecordResponse)
def create_record(
    record: schema.MedicalRecordCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    db_record = models.MedicalRecord(
        patient_id=record.patient_id,
        doctor_id=record.doctor_id,
        diagnosis=record.diagnosis,
        created_at=datetime.utcnow()
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.put("/records/{record_id}", response_model=schema.MedicalRecordResponse)
def update_record(
    record_id: int,
    record: schema.MedicalRecordCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    db_record = db.query(models.MedicalRecord).filter(models.MedicalRecord.record_id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    
    db_record.patient_id = record.patient_id
    db_record.doctor_id = record.doctor_id
    db_record.diagnosis = record.diagnosis
    
    db.commit()
    db.refresh(db_record)
    return db_record

@app.delete("/records/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete records")
    
    db_record = db.query(models.MedicalRecord).filter(models.MedicalRecord.record_id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    
    db.delete(db_record)
    db.commit()
    return {"message": "Medical record deleted successfully"}

# ============= PRESCRIPTIONS ENDPOINTS =============

@app.get("/prescriptions", response_model=List[schema.PrescriptionResponse])
def get_prescriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    prescriptions = db.query(models.Prescription).offset(skip).limit(limit).all()
    return prescriptions

@app.get("/prescriptions/{prescription_id}", response_model=schema.PrescriptionResponse)
def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    prescription = db.query(models.Prescription).filter(models.Prescription.prescription_id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription

@app.post("/prescriptions", response_model=schema.PrescriptionResponse)
def create_prescription(
    prescription: schema.PrescriptionCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    db_prescription = models.Prescription(**prescription.dict())
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

@app.put("/prescriptions/{prescription_id}", response_model=schema.PrescriptionResponse)
def update_prescription(
    prescription_id: int,
    prescription: schema.PrescriptionCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    db_prescription = db.query(models.Prescription).filter(models.Prescription.prescription_id == prescription_id).first()
    if not db_prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    for key, value in prescription.dict().items():
        setattr(db_prescription, key, value)
    
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

@app.delete("/prescriptions/{prescription_id}")
def delete_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete prescriptions")
    
    db_prescription = db.query(models.Prescription).filter(models.Prescription.prescription_id == prescription_id).first()
    if not db_prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    db.delete(db_prescription)
    db.commit()
    return {"message": "Prescription deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)