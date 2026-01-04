from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, database, schema
from database import engine, get_db
import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Patient Service", version="1.0.0")

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
    return {"service": "Patient Service", "status": "running"}

@app.get("/patients", response_model=List[schema.PatientResponse])
def get_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients

@app.get("/patients/{patient_id}", response_model=schema.PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/patients", response_model=schema.PatientResponse)
def create_patient(
    patient: schema.PatientCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.put("/patients/{patient_id}", response_model=schema.PatientResponse)
def update_patient(
    patient_id: int,
    patient: schema.PatientCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    db_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for key, value in patient.dict().items():
        setattr(db_patient, key, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete patients")
    
    db_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)