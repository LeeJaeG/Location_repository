from fastapi import APIRouter, UploadFile, File, HTTPException
from ..service.image_service import image_service

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image file.
    Parameters:
        - file: UploadFile - The image file to upload.
    Returns a JSON response with a success message and the uploaded file name.
    """
    return await image_service.upload_image(file)
