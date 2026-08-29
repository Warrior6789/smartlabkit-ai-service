from fastapi import APIRouter, Depends, UploadFile, File, Query, status
from app.core.config import settings
from app.schemas.detection import DetectionResponse
from app.services.detection_service import DetectionService

router = APIRouter(prefix="/detection", tags=["Detection"])

detection_service_instance = DetectionService()

def get_detection_service() -> DetectionService:
    return detection_service_instance

@router.post("/predict", response_model=DetectionResponse, status_code=status.HTTP_200_OK)
async def predict_components(
    file: UploadFile = File(..., description="Ảnh chụp bo mạch/linh kiện"),
    confidence: float = Query(
        settings.DEFAULT_CONFIDENCE,
        ge=0.0,
        le=1.0,
        description="Ngưỡng tin cậy (Confidence threshold)"
    ),
    service: DetectionService = Depends(get_detection_service)
):
    image_bytes = await file.read()
    
    result = service.detect(image_bytes=image_bytes, conf_threshold=confidence)
    return result