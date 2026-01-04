from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, database, schema
from database import engine, get_db
import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Doctor Service", version="1.0.0")

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
    return {"service": "Doctor Service", "status": "running"}

@app.get("/doctors", response_model=List[schema.DoctorResponse])
def get_doctors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    doctors = db.query(models.Doctor).offset(skip).limit(limit).all()
    return doctors

@app.get("/doctors/{doctor_id}", response_model=schema.DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.post("/doctors", response_model=schema.DoctorResponse)
def create_doctor(
    doctor: schema.DoctorCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@app.put("/doctors/{doctor_id}", response_model=schema.DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor: schema.DoctorCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    for key, value in doctor.dict().items():
        setattr(db_doctor, key, value)
    
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@app.delete("/doctors/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete doctors")
    
    db_doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.delete(db_doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)