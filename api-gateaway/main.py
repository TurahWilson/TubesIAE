from fastapi import FastAPI, Request
import httpx

app = FastAPI()

SERVICE_MAP = {
    "auth": "http://auth-service:8000/graphql",
    "patient": "http://patient-service:8000/graphql",
    "doctor": "http://doctor-service:8000/graphql",
    "medical": "http://medical-service:8000/graphql"
}

@app.post("/{service}")
async def proxy(service: str, req: Request):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            SERVICE_MAP[service],
            json=await req.json(),
            headers=req.headers
        )
        return res.json()
