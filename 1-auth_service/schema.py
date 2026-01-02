import strawberry
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from security import verify_password, create_access_token

@strawberry.type
class AuthPayload:
    access_token: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    def login(self, username: str, password: str) -> AuthPayload:
        db: Session = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password):
            raise Exception("Invalid credentials")

        token = create_access_token({
            "sub": str(user.id),
            "username": user.username,
            "role": user.role
        })
        return AuthPayload(access_token=token)

schema = strawberry.Schema(mutation=Mutation)
