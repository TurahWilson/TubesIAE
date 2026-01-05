import uvicorn
import subprocess
import time
import os
import sys
from fastapi.staticfiles import StaticFiles

def main():
    # Define services and their ports
    # Directory, Port
    services = [
        ("1-auth_service", 8001),
        ("2-patient-service", 8002),
        ("3-doctor-service", 8003),
        ("4-records-service", 8004),
    ]

    procs = []

    print("Starting microservices...")
    for service_dir, port in services:
        print(f"Starting {service_dir} on port {port}...")
        # Run uvicorn in the service directory to ensure local imports work
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "127.0.0.1", 
            "--port", str(port)
        ]
        # We use cwd so 'import database' etc work naturally
        proc = subprocess.Popen(cmd, cwd=service_dir)
        procs.append(proc)

    # Give services a moment to spin up
    print("Waiting for services to initialize...")
    time.sleep(5)

    try:
        print("Configuring API Gateway...")
        # Add api-gateway to path to import app
        gateway_path = os.path.abspath("api-gateway")
        if gateway_path not in sys.path:
            sys.path.append(gateway_path)
            
        from main import app as gateway_app

        # Remove the default root route ("/") from API gateway 
        # so we can serve the frontend index.html there instead
        # Filter out the route with path "/"
        new_routes = [r for r in gateway_app.router.routes if getattr(r, "path", "") != "/"]
        gateway_app.router.routes = new_routes

        # Mount the frontend directory to serve static files
        # html=True allows serving index.html automatically at /
        frontend_path = os.path.abspath("frontend")
        gateway_app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

        print("Starting API Gateway + Frontend on port 8000...")
        # Bind to 0.0.0.0 for Replit exposure
        uvicorn.run(gateway_app, host="0.0.0.0", port=8000)

    except Exception as e:
        print(f"Error starting gateway: {e}")
    finally:
        print("Shutting down services...")
        for p in procs:
            p.terminate()
            p.wait()

if __name__ == "__main__":
    main()
