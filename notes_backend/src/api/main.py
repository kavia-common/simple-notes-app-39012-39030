from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.notes import router as notes_router

app = FastAPI(
    title="Simple Notes API",
    description="A simple FastAPI backend that provides CRUD operations for notes.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Health", "description": "Service health and metadata"},
        {"name": "Notes", "description": "CRUD operations for notes"},
    ],
)

# Enable CORS for development (all origins allowed for simplicity)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["Health"],
    summary="Health check",
    description="Returns service health status.",
)
# PUBLIC_INTERFACE
def health_check():
    """Health check endpoint for liveness probes."""
    return {"status": "ok"}


# Include notes router
app.include_router(notes_router)
