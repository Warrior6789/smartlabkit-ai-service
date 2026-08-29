from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.detection_router import router as detection_router
from app.api.v1.datasheet_router import router as datasheet_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Microservice nhận diện linh kiện và phân tích mạch thí nghiệm cho SmartLabKit",
    version="1.0.0"
)

app.include_router(detection_router, prefix=settings.API_V1_STR)
app.include_router(datasheet_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "model": settings.MODEL_PATH
    }