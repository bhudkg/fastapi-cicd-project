
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.api.items import router as items_router
from app.db.session import check_database_connection

app = FastAPI(
    title="Production FastAPI API",
    description="FastAPI application with CI/CD integration",
    version="1.0.0",
)

app.include_router(items_router)


@app.get("/")
async def home():
    return {
        "message": "Welcome to Production FastAPI",
        "version": "1.0.0",
    }


@app.get("/health/live")
async def health():
    return {"status": "alive"}


@app.get("/health/ready")
def readiness():
    try:
        check_database_connection()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable",
        )

    return {"status": "ready", "database": "connected"}
