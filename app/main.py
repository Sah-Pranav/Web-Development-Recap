from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.health import router as health_router
from app.core.logging import logger
from app.core.middleware import error_handling_middleware

app = FastAPI(title="AI Power RAG Chatbot", version="0.1.0")

# Include API routers
app.include_router(health_router, prefix="/api")

# Add middleware
app.middleware("http")(error_handling_middleware)

# Optional: CORS setup for frontend apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod, replace '*' with allowed domains
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to AI Power RAG Chatbot!"}

@app.get("/error")
def simulate_error():
    raise ValueError("This is a test error")

