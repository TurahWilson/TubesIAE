from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from database import Base, engine
from schema import schema

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")
app.include_router(GraphQLRouter(schema), prefix="/graphql")
