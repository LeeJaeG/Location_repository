import os
import uuid
from fastapi import UploadFile, HTTPException
from ..core.settings import settings

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class ImageService:
    def __init__(self):
        self.upload_dir = settings.upload_dir

    async def upload_image(self, file: UploadFile):
        try:
            upload_dir = self.upload_dir
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            extension = file.filename.split('.')[-1].lower()
            if extension not in ALLOWED_EXTENSIONS:
                raise HTTPException(status_code=400, detail="Invalid image extension")

            filename = f"{uuid.uuid4()}.{extension}"
            contents = await file.read()
            with open(os.path.join(upload_dir, filename), "wb") as f:
                f.write(contents)
            
            return {"message": "Image uploaded successfully", "file": filename}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
        
image_service = ImageService()