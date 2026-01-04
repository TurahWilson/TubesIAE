# Auth Service

Service untuk autentikasi dan manajemen user dengan JWT.

## Files
- `main.py` - Main application dengan endpoints auth
- `models.py` - User model (SQLAlchemy)
- `schema.py` - Pydantic schemas untuk validation
- `database.py` - Database connection setup
- `security.py` - Password hashing & JWT utilities
- `config.py` - Configuration settings
- `requirment.txt` - Python dependencies
- `Dockerfile` - Docker container setup

## Endpoints
- POST `/register` - Register user baru
- POST `/token` - Login dan dapatkan JWT token
- GET `/me` - Get user profile
- POST `/verify-token` - Verify JWT token

## Database
Database: `hospital_auth`
Table: `users`
- id (PK)
- email (unique)
- full_name
- hashed_password
- role (admin/user)
- created_at
- updated_at

## Run Locally
```bash
pip install -r requirment.txt
python main.py
```

Buka: http://localhost:8001/docs