from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI(title="Hospital API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://localhost:8001"),
    "patients": os.getenv("PATIENT_SERVICE_URL", "http://localhost:8002"),
    "doctors": os.getenv("DOCTOR_SERVICE_URL", "http://localhost:8003"),
    "records": os.getenv("RECORDS_SERVICE_URL", "http://localhost:8004"),
}

async def forward_request(service: str, path: str, request: Request):
    service_url = SERVICES.get(service)
    if not service_url:
        raise HTTPException(status_code=404, detail="Service not found")
    
    url = f"{service_url}{path}"
    headers = dict(request.headers)
    headers.pop("host", None)
    
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=request.query_params
            )
            return JSONResponse(
                content=response.json() if response.content else None,
                status_code=response.status_code
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_gateway(path: str, request: Request):
    return await forward_request("auth", f"/{path}", request)

@app.api_route("/patients/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def patients_gateway(path: str, request: Request):
    return await forward_request("patients", f"/{path}", request)

@app.api_route("/doctors/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def doctors_gateway(path: str, request: Request):
    return await forward_request("doctors", f"/{path}", request)

@app.api_route("/records/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def records_gateway(path: str, request: Request):
    return await forward_request("records", f"/{path}", request)

@app.get("/")
def read_root():
    return {
        "message": "Hospital API Gateway",
        "version": "1.0.0",
        "services": list(SERVICES.keys()),
        "endpoints": {
            "auth": "/auth/*",
            "patients": "/patients/*",
            "doctors": "/doctors/*",
            "records": "/records/*"
        }
    }

@app.get("/health")
async def health_check():
    health_status = {}
    async with httpx.AsyncClient() as client:
        for service_name, service_url in SERVICES.items():
            try:
                response = await client.get(f"{service_url}/", timeout=5.0)
                health_status[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "url": service_url,
                    "status_code": response.status_code
                }
            except Exception as e:
                health_status[service_name] = {
                    "status": "down",
                    "url": service_url,
                    "error": str(e)
                }
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)