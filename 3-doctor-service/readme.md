# Doctor Service

Service untuk manajemen data dokter.

## Files
- `main.py` - Main application dengan CRUD endpoints
- `models.py` - Doctor model (SQLAlchemy)
- `schema.py` - Pydantic schemas untuk validation
- `database.py` - Database connection setup
- `config.py` - Configuration settings
- `requirment.txt` - Python dependencies
- `Dockerfile` - Docker container setup

## Endpoints
- GET `/doctors` - List all doctors
- GET `/doctors/{id}` - Get doctor detail
- POST `/doctors` - Create new doctor
- PUT `/doctors/{id}` - Update doctor
- DELETE `/doctors/{id}` - Delete doctor (admin only)

## Database
Database: `hospital_doctors`
Table: `doctors`
- doctor_id (PK)
- name
- specialization
- phone_number
- email (unique)
- license_number (unique)

## Run Locally
```bash
pip install -r requirment.txt
python main.py
```

Buka: http://localhost:8003/docs