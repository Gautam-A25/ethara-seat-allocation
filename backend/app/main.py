from fastapi import FastAPI

app = FastAPI(
    title="Ethara Seat Allocation API",
    version="1.0.0",
    description="Backend API for the Ethara Seat Allocation & Project Mapping System"
)


@app.get("/")
def root():
    return {
        "message": "Ethara Seat Allocation API is running."
    }