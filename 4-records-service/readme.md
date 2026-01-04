# Records Service

Service untuk manajemen rekam medis dan resep obat.

## Files
- `main.py` - Main application dengan CRUD endpoints
- `models.py` - MedicalRecord & Prescription models (SQLAlchemy)
- `schema.py` - Pydantic schemas untuk validation
- `database.py` - Database connection setup
- `config.py` - Configuration settings
- `requirment.txt` - Python dependencies
- `Dockerfile` - Docker container setup

## Endpoints

### Medical Records
- GET `/records` - List all medical records
- GET `/records/{id}` - Get record detail
- POST `/records` - Create new record
- PUT `/records/{id}` - Update record
- DELETE `/records/{id}` - Delete record (admin only)

### Prescriptions
- GET `/prescriptions` - List all prescriptions
- GET `/prescriptions/{id}` - Get prescription detail
- POST `/prescriptions` - Create new prescription
- PUT `/prescriptions/{id}` - Update prescription
- DELETE `/prescriptions/{id}` - Delete prescription (admin only)

## Database
Database: `hospital_records`

Table: `medical_records`
- record_id (PK)
- patient_id (FK to patients)
- doctor_id (FK to doctors)
- diagnosis
- created_at

Table: `prescriptions`
- prescription_id (PK)
- record_id (FK to medical_records)
- dosage
- instructions
- medicine_recipe

## Run Locally
```bash
pip install -r requirment.txt
python main.py
```

Buka: http://localhost:8004/docs