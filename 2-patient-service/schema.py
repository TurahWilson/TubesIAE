import strawberry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Patient, Base
from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

@strawberry.type
class PatientType:
    id: int
    name: str
    email: str
    phone: str
    gender: str
    address: str

@strawberry.type
class Query:
    @strawberry.field
    def patients(self) -> list[PatientType]:
        db = SessionLocal()
        return db.query(Patient).all()

    @strawberry.field
    def patient(self, id: int) -> PatientType | None:
        db = SessionLocal()
        return db.query(Patient).filter(Patient.id == id).first()

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_patient(
        self,
        name: str,
        email: str,
        phone: str,
        gender: str,
        address: str
    ) -> PatientType:
        db = SessionLocal()

        patient = Patient(
            name=name,
            email=email,
            phone=phone,
            gender=gender,
            address=address
        )

        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient

schema = strawberry.Schema(query=Query, mutation=Mutation)
