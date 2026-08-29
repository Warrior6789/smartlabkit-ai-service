from typing import List
from pydantic import BaseModel

class BoundingBox(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float

class DetectedItem(BaseModel):
    component_name: str
    confidence: float
    box: BoundingBox

class DetectionResponse(BaseModel):
    success: bool
    total_detected: int
    data: List[DetectedItem]