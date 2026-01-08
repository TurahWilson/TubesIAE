
import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
import models

@strawberry.type
class MedicineItem:
    name: str
    qty: int

@strawberry.type
class PrescriptionResult:
    isValid: bool
    patientName: Optional[str]
    medicines: Optional[List[MedicineItem]]

def get_prescription_validation(id: str, db: Session) -> PrescriptionResult:
    # Try to find the prescription by ID
    try:
        # Assuming ID passed is convertible to int as per database model
        print(f"Validating prescription id: {id}") # Debug log
        prescription_id = int(id)
        
        prescription = db.query(models.Prescription).filter(models.Prescription.id == prescription_id).first()
        
        if not prescription:
            return PrescriptionResult(isValid=False, patientName=None, medicines=None)
        
        # Convert items
        medicine_items = []
        for item in prescription.items:
            medicine_items.append(
                MedicineItem(
                    name=item.medicineName,
                    qty=item.quantity
                )
            )
            
        return PrescriptionResult(
            isValid=True,
            patientName=prescription.patientName,
            medicines=medicine_items
        )
            
    except ValueError:
        # If id cannot be converted to int
        return PrescriptionResult(isValid=False, patientName=None, medicines=None)
    except Exception as e:
        print(f"Error validating prescription: {e}")
        return PrescriptionResult(isValid=False, patientName=None, medicines=None)

@strawberry.type
class PrescriptionUpdateResult:
    success: bool
    message: str

def update_prescription_status(id: str, status: str, db: Session) -> PrescriptionUpdateResult:
    try:
        print(f"Updating prescription id: {id} to status: {status}")
        prescription_id = int(id)
        prescription = db.query(models.Prescription).filter(models.Prescription.id == prescription_id).first()
        
        if not prescription:
            return PrescriptionUpdateResult(success=False, message="Prescription not found")
        
        prescription.status = status
        db.commit()
        db.refresh(prescription)
        
        return PrescriptionUpdateResult(success=True, message=f"Status updated to {status}")
    except ValueError:
        return PrescriptionUpdateResult(success=False, message="Invalid ID format")
    except Exception as e:
        print(f"Error updating prescription: {e}")
        return PrescriptionUpdateResult(success=False, message=str(e))

@strawberry.type
class Query:
    @strawberry.field
    def validatePrescription(self, id: str, info) -> PrescriptionResult:
        db = info.context["db"]
        return get_prescription_validation(id, db)

@strawberry.type
class Mutation:
    @strawberry.field
    def updatePrescriptionStatus(self, id: str, status: str, info) -> PrescriptionUpdateResult:
        db = info.context["db"]
        return update_prescription_status(id, status, db)

schema = strawberry.Schema(query=Query, mutation=Mutation)
