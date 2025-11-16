from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from database import Base, engine
import auth, teachers, schools, payments, jobs
import uvicorn
import traceback
from pathlib import Path

# Import routes later
app = FastAPI(title="Edumentor MVP API")

# Configure CORS - Allow all origins including null (local file://)
app.add_middleware(
    CORSMiddleware, 
    allow_origins=[
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"  # Allow all other origins as well
    ],
    allow_credentials=False,  # Set to False when using "*" origins
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Error: {exc}")
    print(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc),
            "path": str(request.url)
        }
    )

Base.metadata.create_all(bind=engine)
# Include routes
app.include_router(auth.router)
app.include_router(teachers.router)
app.include_router(schools.router)
app.include_router(payments.router)
app.include_router(jobs.router)

@app.get("/")
def home():
    return {"message": "Welcome to Edumentor MVP API"}

# Serve static HTML files from project root
static_dir = Path(__file__).parent.parent
html_files = [
    'index.html', 'login.html', 'teacher-register.html', 'teacher-payment.html',
    'payment-success.html', 'school-register.html', 'teacher-dashboard.html',
    'school-dashboard.html', 'teacher-listings.html'
]

# Create route for each HTML file to serve directly
for html in html_files:
    file_path = static_dir / html
    if file_path.exists():
        @app.get(f"/{html}")
        def serve_file(file_path=file_path):
            return FileResponse(file_path, media_type="text/html")



if __name__ == "__main__":
    # Local development convenience: only run uvicorn when this module is executed directly.
    # For production use, run with an ASGI server: e.g. `uvicorn routes.main:app --host 0.0.0.0 --port 8000 --workers 4`
    uvicorn.run(app, host="127.0.0.1", port=8000)