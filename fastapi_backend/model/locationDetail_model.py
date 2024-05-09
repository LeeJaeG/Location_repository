from typing import Optional
from pydantic import BaseModel

class LocationDetail(BaseModel):  # Changed class name from Location_detail to LocationDetail
    location_object_id: str
    location_type: str
    geo_coordinates: Optional[str] = None
    building_address: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None
    x: Optional[float] = None
    y: Optional[float] = None
    image_path: Optional[str] = None
    location_path: Optional[str] = None
    location_parent_id: Optional[str] = None