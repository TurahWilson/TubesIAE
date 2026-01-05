const API_URL = 'http://127.0.0.1:8000';
let authToken = localStorage.getItem('authToken');
let userRole = localStorage.getItem('userRole');
let userEmail = localStorage.getItem('userEmail');

// Show/Hide Login and Register Forms
document.getElementById('showRegister').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
});

document.getElementById('showLogin').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('loginForm').style.display = 'block';
});

// Register
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const userData = {
        email: document.getElementById('registerEmail').value,
        full_name: document.getElementById('registerName').value,
        password: document.getElementById('registerPassword').value,
        role: document.getElementById('registerRole').value
    };

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            alert('Registration successful! Please login.');
            document.getElementById('showLogin').click();
            document.getElementById('registerForm').reset();
        } else {
            const error = await response.json();
            alert('Registration failed: ' + error.detail);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Login
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append('username', document.getElementById('loginEmail').value);
    formData.append('password', document.getElementById('loginPassword').value);

    try {
        const response = await fetch(`${API_URL}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            userRole = data.role;

            localStorage.setItem('authToken', authToken);
            localStorage.setItem('userRole', userRole);
            localStorage.setItem('userEmail', document.getElementById('loginEmail').value);

            showDashboard();
        } else {
            alert('Login failed! Please check your credentials.');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Logout
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userEmail');
    location.reload();
});

// Show Dashboard
function showDashboard() {
    document.getElementById('loginPage').style.display = 'none';
    document.getElementById('dashboardPage').style.display = 'block';
    document.getElementById('userName').textContent = localStorage.getItem('userEmail');

    // UI Access Control
    if (userRole !== 'admin') {
        const addButtons = ['btnAddPatient', 'btnAddDoctor', 'btnAddRecord', 'btnAddPrescription'];
        addButtons.forEach(id => {
            const btn = document.getElementById(id);
            if (btn) btn.style.display = 'none';
        });
    }

    loadDashboardData();
}

// Check if already logged in
if (authToken) {
    showDashboard();
}

// Load Dashboard Data
async function loadDashboardData() {
    try {
        // Load patients count
        const patientsResponse = await fetch(`${API_URL}/patients/patients`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        if (patientsResponse.ok) {
            const patients = await patientsResponse.json();
            document.getElementById('totalPatients').textContent = patients.length;
        }

        // Load doctors count
        const doctorsResponse = await fetch(`${API_URL}/doctors/doctors`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        if (doctorsResponse.ok) {
            const doctors = await doctorsResponse.json();
            document.getElementById('totalDoctors').textContent = doctors.length;
        }

        // Load records count
        const recordsResponse = await fetch(`${API_URL}/records/records`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        if (recordsResponse.ok) {
            const records = await recordsResponse.json();
            document.getElementById('totalRecords').textContent = records.length;
        }

        // Load prescriptions count
        const prescriptionsResponse = await fetch(`${API_URL}/records/prescriptions`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        if (prescriptionsResponse.ok) {
            const prescriptions = await prescriptionsResponse.json();
            document.getElementById('totalPrescriptions').textContent = prescriptions.length;
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

// Helper function to show content based on page
function showPage(page) {
    // Update active link
    document.querySelectorAll('.sidebar .nav-link').forEach(l => l.classList.remove('active'));
    const correspondingNavLink = document.querySelector(`.sidebar .nav-link[data-page="${page}"]`);
    if (correspondingNavLink) {
        correspondingNavLink.classList.add('active');
    }

    // Show content
    document.querySelectorAll('#contentArea > div').forEach(div => div.style.display = 'none');

    if (page === 'dashboard') {
        document.getElementById('dashboardContent').style.display = 'block';
        loadDashboardData(); // Reload dashboard data when navigating to it
    } else if (page === 'patients') {
        document.getElementById('patientsContent').style.display = 'block';
        loadPatients();
    } else if (page === 'doctors') {
        document.getElementById('doctorsContent').style.display = 'block';
        loadDoctors();
    } else if (page === 'records') {
        document.getElementById('recordsContent').style.display = 'block';
        loadRecords();
    } else if (page === 'prescriptions') {
        document.getElementById('prescriptionsContent').style.display = 'block';
        loadPrescriptions();
    }
}

// Navigation
document.querySelectorAll('.sidebar .nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = e.currentTarget.getAttribute('data-page');
        if (page) {
            showPage(page);
        }
    });
});

// Dashboard Card Navigation
document.querySelectorAll('.dashboard-card-link').forEach(card => {
    card.addEventListener('click', () => {
        const page = card.getAttribute('data-page');
        if (page) {
            showPage(page);
        }
    });
});

// ========== PATIENTS ==========

async function loadPatients() {
    try {
        const response = await fetch(`${API_URL}/patients/patients`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            const patients = await response.json();
            const tbody = document.querySelector('#patientsTable tbody');
            tbody.innerHTML = '';

            patients.forEach(patient => {
                const row = `
                    <tr>
                        <td>${patient.patient_id}</td>
                        <td>${patient.name}</td>
                        <td>${patient.email}</td>
                        <td>${patient.phone_number}</td>
                        <td>${patient.gender}</td>
                        <td>${patient.address}</td>
                        <td>
                            <button class="btn btn-sm btn-info" onclick="viewPatient(${patient.patient_id})">
                                <i class="fas fa-eye"></i>
                            </button>
                            ${userRole === 'admin' ? `
                            <button class="btn btn-sm btn-danger" onclick="deletePatient(${patient.patient_id})">
                                <i class="fas fa-trash"></i>
                            </button>
                            ` : ''}
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        }
    } catch (error) {
        console.error('Error loading patients:', error);
    }
}

document.getElementById('addPatientForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const patientData = {
        name: document.getElementById('patientName').value,
        email: document.getElementById('patientEmail').value,
        phone_number: document.getElementById('patientPhone').value,
        gender: document.getElementById('patientGender').value,
        address: document.getElementById('patientAddress').value
    };

    try {
        const response = await fetch(`${API_URL}/patients/patients`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(patientData)
        });

        if (response.ok) {
            alert('Patient added successfully!');
            document.getElementById('addPatientForm').reset();
            bootstrap.Modal.getInstance(document.getElementById('addPatientModal')).hide();
            loadPatients();
            loadDashboardData();
        } else {
            const error = await response.json();
            alert('Failed to add patient: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

async function deletePatient(patientId) {
    if (!confirm('Are you sure you want to delete this patient?')) return;

    try {
        const response = await fetch(`${API_URL}/patients/patients/${patientId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            alert('Patient deleted successfully!');
            loadPatients();
            loadDashboardData();
        } else {
            alert('Failed to delete patient!');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function viewPatient(patientId) {
    try {
        const response = await fetch(`${API_URL}/patients/patients/${patientId}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            const patient = await response.json();
            document.getElementById('viewPatientId').textContent = patient.patient_id;
            document.getElementById('viewPatientName').textContent = patient.name;
            document.getElementById('viewPatientEmail').textContent = patient.email;
            document.getElementById('viewPatientPhone').textContent = patient.phone_number;
            document.getElementById('viewPatientGender').textContent = patient.gender;
            document.getElementById('viewPatientAddress').textContent = patient.address;
            new bootstrap.Modal(document.getElementById('viewPatientModal')).show();
        } else {
            const error = await response.json();
            alert('Failed to fetch patient details: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ========== DOCTORS ==========

async function loadDoctors() {
    try {
        const response = await fetch(`${API_URL}/doctors/doctors`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            const doctors = await response.json();
            const tbody = document.querySelector('#doctorsTable tbody');
            tbody.innerHTML = '';

            doctors.forEach(doctor => {
                const row = `
                    <tr>
                        <td>${doctor.doctor_id}</td>
                        <td>${doctor.name}</td>
                        <td>${doctor.specialization}</td>
                        <td>${doctor.email}</td>
                        <td>${doctor.phone_number}</td>
                        <td>${doctor.license_number}</td>
                        <td>
                            <button class="btn btn-sm btn-info" onclick="viewDoctor(${doctor.doctor_id})">
                                <i class="fas fa-eye"></i>
                            </button>
                            ${userRole === 'admin' ? `
                            <button class="btn btn-sm btn-danger" onclick="deleteDoctor(${doctor.doctor_id})">
                                <i class="fas fa-trash"></i>
                            </button>
                            ` : ''}
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        }
    } catch (error) {
        console.error('Error loading doctors:', error);
    }
}

document.getElementById('addDoctorForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const doctorData = {
        name: document.getElementById('doctorName').value,
        specialization: document.getElementById('doctorSpecialization').value,
        email: document.getElementById('doctorEmail').value,
        phone_number: document.getElementById('doctorPhone').value,
        license_number: document.getElementById('doctorLicense').value
    };

    try {
        const response = await fetch(`${API_URL}/doctors/doctors`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(doctorData)
        });

        if (response.ok) {
            alert('Doctor added successfully!');
            document.getElementById('addDoctorForm').reset();
            bootstrap.Modal.getInstance(document.getElementById('addDoctorModal')).hide();
            loadDoctors();
            loadDashboardData();
        } else {
            const error = await response.json();
            alert('Failed to add doctor: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

async function deleteDoctor(doctorId) {
    if (!confirm('Are you sure you want to delete this doctor?')) return;

    try {
        const response = await fetch(`${API_URL}/doctors/doctors/${doctorId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            alert('Doctor deleted successfully!');
            loadDoctors();
            loadDashboardData();
        } else {
            alert('Failed to delete doctor!');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function viewDoctor(doctorId) {
    try {
        const response = await fetch(`${API_URL}/doctors/doctors/${doctorId}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            const doctor = await response.json();
            document.getElementById('viewDoctorId').textContent = doctor.doctor_id;
            document.getElementById('viewDoctorName').textContent = doctor.name;
            document.getElementById('viewDoctorSpecialization').textContent = doctor.specialization;
            document.getElementById('viewDoctorEmail').textContent = doctor.email;
            document.getElementById('viewDoctorPhone').textContent = doctor.phone_number;
            document.getElementById('viewDoctorLicense').textContent = doctor.license_number;
            new bootstrap.Modal(document.getElementById('viewDoctorModal')).show();
        } else {
            const error = await response.json();
            alert('Failed to fetch doctor details: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ========== MEDICAL RECORDS ==========

async function loadRecords() {
    try {
        const response = await fetch(`${API_URL}/records/records`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            const records = await response.json();
            const tbody = document.querySelector('#recordsTable tbody');
            tbody.innerHTML = '';

            records.forEach(record => {
                const date = new Date(record.created_at).toLocaleString();
                const row = `
                    <tr>
                        <td>${record.record_id}</td>
                        <td>${record.patient_id}</td>
                        <td>${record.doctor_id}</td>
                        <td>${record.diagnosis}</td>
                        <td>${date}</td>
                        <td>
                            <button class="btn btn-sm btn-info" onclick="viewRecord(${record.record_id})">
                                <i class="fas fa-eye"></i>
                            </button>
                            ${userRole === 'admin' ? `
                            <button class="btn btn-sm btn-danger" onclick="deleteRecord(${record.record_id})">
                                <i class="fas fa-trash"></i>
                            </button>
                            ` : ''}
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        }
    } catch (error) {
        console.error('Error loading records:', error);
    }
}

document.getElementById('addRecordForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const recordData = {
        patient_id: parseInt(document.getElementById('recordPatientId').value),
        doctor_id: parseInt(document.getElementById('recordDoctorId').value),
        diagnosis: document.getElementById('recordDiagnosis').value
    };

    try {
        const response = await fetch(`${API_URL}/records/records`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(recordData)
        });

        if (response.ok) {
            alert('Medical record added successfully!');
            document.getElementById('addRecordForm').reset();
            bootstrap.Modal.getInstance(document.getElementById('addRecordModal')).hide();
            loadRecords();
            loadDashboardData();
        } else {
            const error = await response.json();
            alert('Failed to add medical record: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

async function deleteRecord(recordId) {
    if (!confirm('Are you sure you want to delete this record?')) return;

    try {
        const response = await fetch(`${API_URL}/records/records/${recordId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            alert('Record deleted successfully!');
            loadRecords();
            loadDashboardData();
        } else {
            alert('Failed to delete record!');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function viewRecord(recordId) {
    try {
        const response = await fetch(`${API_URL}/records/records/${recordId}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            const record = await response.json();
            document.getElementById('viewRecordId').textContent = record.record_id;
            document.getElementById('viewRecordPatientId').textContent = record.patient_id;
            document.getElementById('viewRecordDoctorId').textContent = record.doctor_id;
            document.getElementById('viewRecordDiagnosis').textContent = record.diagnosis;
            document.getElementById('viewRecordDate').textContent = new Date(record.created_at).toLocaleString();
            new bootstrap.Modal(document.getElementById('viewRecordModal')).show();
        } else {
            const error = await response.json();
            alert('Failed to fetch record details: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ========== PRESCRIPTIONS ==========

async function loadPrescriptions() {
    try {
        const response = await fetch(`${API_URL}/records/prescriptions`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            const prescriptions = await response.json();
            const tbody = document.querySelector('#prescriptionsTable tbody');
            tbody.innerHTML = '';

            prescriptions.forEach(prescription => {
                const row = `
                    <tr>
                        <td>${prescription.prescription_id}</td>
                        <td>${prescription.record_id}</td>
                        <td>${prescription.medicine_recipe}</td>
                        <td>${prescription.dosage}</td>
                        <td>${prescription.instructions}</td>
                        <td>
                            <button class="btn btn-sm btn-info" onclick="viewPrescription(${prescription.prescription_id})">
                                <i class="fas fa-eye"></i>
                            </button>
                            ${userRole === 'admin' ? `
                            <button class="btn btn-sm btn-danger" onclick="deletePrescription(${prescription.prescription_id})">
                                <i class="fas fa-trash"></i>
                            </button>
                            ` : ''}
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        }
    } catch (error) {
        console.error('Error loading prescriptions:', error);
    }
}

document.getElementById('addPrescriptionForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const prescriptionData = {
        record_id: parseInt(document.getElementById('prescriptionRecordId').value),
        dosage: document.getElementById('prescriptionDosage').value,
        instructions: document.getElementById('prescriptionInstructions').value,
        medicine_recipe: document.getElementById('prescriptionMedicine').value
    };

    try {
        const response = await fetch(`${API_URL}/records/prescriptions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(prescriptionData)
        });

        if (response.ok) {
            alert('Prescription added successfully!');
            document.getElementById('addPrescriptionForm').reset();
            bootstrap.Modal.getInstance(document.getElementById('addPrescriptionModal')).hide();
            loadPrescriptions();
            loadDashboardData();
        } else {
            const error = await response.json();
            alert('Failed to add prescription: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

async function deletePrescription(prescriptionId) {
    if (!confirm('Are you sure you want to delete this prescription?')) return;

    try {
        const response = await fetch(`${API_URL}/records/prescriptions/${prescriptionId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            alert('Prescription deleted successfully!');
            loadPrescriptions();
            loadDashboardData();
        } else {
            alert('Failed to delete prescription!');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function viewPrescription(prescriptionId) {
    try {
        const response = await fetch(`${API_URL}/records/prescriptions/${prescriptionId}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            const prescription = await response.json();
            document.getElementById('viewPrescriptionId').textContent = prescription.prescription_id;
            document.getElementById('viewPrescriptionRecordId').textContent = prescription.record_id;
            document.getElementById('viewPrescriptionMedicine').textContent = prescription.medicine_recipe;
            document.getElementById('viewPrescriptionDosage').textContent = prescription.dosage;
            document.getElementById('viewPrescriptionInstructions').textContent = prescription.instructions;
            new bootstrap.Modal(document.getElementById('viewPrescriptionModal')).show();
        } else {
            const error = await response.json();
            alert('Failed to fetch prescription details: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}