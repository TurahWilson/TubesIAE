-- Create databases
CREATE DATABASE hospital_auth;
CREATE DATABASE hospital_patients;
CREATE DATABASE hospital_doctors;
CREATE DATABASE hospital_records;

-- Connect to hospital_auth
\c hospital_auth;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Connect to hospital_patients
\c hospital_patients;

CREATE TABLE IF NOT EXISTS patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    address TEXT NOT NULL
);

INSERT INTO patients (name, email, phone_number, gender, address) VALUES 
('John Doe', 'john.doe@email.com', '081234567890', 'Male', 'Jl. Merdeka No. 123, Jakarta'),
('Jane Smith', 'jane.smith@email.com', '081234567891', 'Female', 'Jl. Sudirman No. 456, Jakarta');

-- Connect to hospital_doctors
\c hospital_doctors;

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    specialization VARCHAR(255) NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    license_number VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO doctors (name, specialization, phone_number, email, license_number) VALUES 
('Dr. Sarah Wilson', 'Cardiology', '081234560001', 'dr.sarah@hospital.com', 'DOC-2024-001'),
('Dr. Michael Chen', 'Pediatrics', '081234560002', 'dr.michael@hospital.com', 'DOC-2024-002');

-- Connect to hospital_records
\c hospital_records;

CREATE TABLE IF NOT EXISTS medical_records (
    record_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    diagnosis TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    record_id INTEGER NOT NULL,
    dosage VARCHAR(255) NOT NULL,
    instructions TEXT NOT NULL,
    medicine_recipe TEXT NOT NULL
);

INSERT INTO medical_records (patient_id, doctor_id, diagnosis) VALUES 
(1, 1, 'Hypertension - High blood pressure detected'),
(2, 2, 'Common Cold - Viral infection');

INSERT INTO prescriptions (record_id, dosage, instructions, medicine_recipe) VALUES 
(1, '10mg once daily', 'Take with food in the morning', 'Amlodipine 10mg - 30 tablets'),
(2, '500mg three times daily', 'Take after meals for 5 days', 'Paracetamol 500mg - 15 tablets');