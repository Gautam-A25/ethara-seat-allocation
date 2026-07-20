from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine

app = FastAPI(
    title="Ethara Seat Allocation API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "API Running"}


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "Database Connected"
        }
    except Exception as e:
        return {
            "status": "Connection Failed",
            "error": str(e)
        }