from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
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
    headers.pop("content-length", None) 
    
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
            # Return raw content to preserve original response (HTML, Text, or JSON)
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except Exception as e:
            # More robust error handling for JSON decode
            try:
                error_content = {"detail": str(e)}
            except:
                error_content = {"detail": "Unknown error in gateway"}
            raise HTTPException(status_code=500, detail=str(e))

# --- ROUTES ---

@app.api_route("/api/prescriptions/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def prescriptions_gateway(path: str, request: Request):
    # Route /api/prescriptions/XYZ -> records-service /prescriptions/XYZ
    # Handle root case /api/prescriptions -> records-service /prescriptions
    if path == "":
         return await forward_request("records", "/prescriptions", request)
    return await forward_request("records", f"/prescriptions/{path}", request)

# Catch-all for /api/prescriptions (without trailing slash or path)
@app.api_route("/api/prescriptions", methods=["GET", "POST"])
async def prescriptions_root_gateway(request: Request):
    return await forward_request("records", "/prescriptions", request)


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
    return {"message": "Hospital API Gateway ready"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)