# Patient Service

Service untuk manajemen data pasien.

## Files
- `main.py` - Main application dengan CRUD endpoints
- `models.py` - Patient model (SQLAlchemy)
- `schema.py` - Pydantic schemas untuk validation
- `database.py` - Database connection setup
- `config.py` - Configuration settings
- `requirment.txt` - Python dependencies
- `Dockerfile` - Docker container setup

## Endpoints
- GET `/patients` - List all patients
- GET `/patients/{id}` - Get patient detail
- POST `/patients` - Create new patient
- PUT `/patients/{id}` - Update patient
- DELETE `/patients/{id}` - Delete patient (admin only)

## Database
Database: `hospital_patients`
Table: `patients`
- patient_id (PK)
- name
- email (unique)
- phone_number
- gender
- address

## Run Locally
```bash
pip install -r requirment.txt
python main.py
```

Buka: http://localhost:8002/docs