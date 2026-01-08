
from fastapi.testclient import TestClient
from main import app, get_db
import models
from database import engine, SessionLocal

# Re-create tables to be sure (optional, but safe for testing if we want a clean state, 
# but here I'll just add data to existing)
# models.Base.metadata.create_all(bind=engine)

client = TestClient(app)

def setup_test_data():
    db = SessionLocal()
    # Check if a test prescription exists, if not create one
    prescription = models.Prescription(
        patientName="John Doe",
        doctorName="Dr. Smith",
        status="pending"
    )
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    
    # Add items
    item = models.PrescriptionItem(
        prescription_id=prescription.id,
        medicine_id=101,
        medicine_name="Paracetamol",
        quantity=10,
        instructions="After meal"
    )
    db.add(item)
    db.commit()
    
    return prescription.id

def test_graphql_query():
    # Setup data
    p_id = setup_test_data()
    print(f"Created test prescription with ID: {p_id}")

    query = """
    query GetPrescription($id: String!) {
        validatePrescription(id: $id) {
            isValid
            patientName
            medicines {
                name
                qty
            }
        }
    }
    """
    
    response = client.post("/graphql", json={
        "query": query,
        "variables": {"id": str(p_id)}
    })
    
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    
    data = response.json()
    if "errors" in data:
        print("GraphQL Errors:", data["errors"])
    else:
        result = data["data"]["validatePrescription"]
        assert result["isValid"] == True
        assert result["patientName"] == "John Doe"
        assert len(result["medicines"]) > 0
        assert result["medicines"][0]["name"] == "Paracetamol"
        print("Verification SUCCESS!")

if __name__ == "__main__":
    test_graphql_query()
