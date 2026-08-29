from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.datasheet import DatasheetParseResponse
from app.services.datasheet_service import DatasheetService

router = APIRouter()
datasheet_service = DatasheetService()

@router.post("/parse", response_model=DatasheetParseResponse)
async def parse_datasheet(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file định dạng PDF.")
    
    pdf_bytes = await file.read()
    response = await datasheet_service.parse(pdf_bytes)
    return response