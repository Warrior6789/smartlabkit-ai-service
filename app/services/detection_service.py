import io
from typing import List
from PIL import Image
from ultralytics import YOLO

from app.core.config import settings
from app.schemas.detection import BoundingBox, DetectedItem, DetectionResponse

class DetectionService:
    def __init__(self, model_path: str = settings.MODEL_PATH):
        self.model = YOLO(model_path)
        print(f"[AI Service] Loaded YOLO model from: {model_path}")

    def detect(self, image_bytes: bytes, conf_threshold: float = settings.DEFAULT_CONFIDENCE) -> DetectionResponse:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        results = self.model.predict(source=image, conf=conf_threshold, verbose=False)

        items: List[DetectedItem] = []

        if results and len(results) > 0:
            result = results[0]
            for box in result.boxes:
                coords = box.xyxy[0].tolist()
                x_min, y_min, x_max, y_max = coords[0], coords[1], coords[2], coords[3]

                confidence = float(box.conf[0])
                cls_id = int(box.cls[0])
                component_name = self.model.names[cls_id]

                items.append(
                    DetectedItem(
                        component_name=component_name,
                        confidence=round(confidence, 3),
                        box=BoundingBox(
                            x_min=round(x_min, 2),
                            y_min=round(y_min, 2),
                            x_max=round(x_max, 2),
                            y_max=round(y_max, 2)
                        )
                    )
                )

        return DetectionResponse(
            success=True,
            total_detected=len(items),
            data=items
        )