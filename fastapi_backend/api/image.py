from fastapi import APIRouter, UploadFile, File, HTTPException
from ..service.image_service import image_service

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    return await image_service.upload_image(file)

