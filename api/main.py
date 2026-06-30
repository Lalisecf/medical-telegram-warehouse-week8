from fastapi import FastAPI

app = FastAPI(
    title="Medical Telegram Warehouse API",
    description="Analytical API for Telegram warehouse",
    version="1.0.0"
)


@app.get("/")
def root():

    return {
        "message": "Medical Telegram Warehouse API",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }