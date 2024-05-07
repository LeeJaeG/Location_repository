from fastapi import APIRouter, status
from typing import List
from ..model.location_model import LocationDetail
from ..db.database import MongoLocationDetailRepository

router = APIRouter()

@router.get("/api/physical_layer/locations_detail/{location_object_id}", response_model=LocationDetail, response_model_exclude_unset=True)
async def get_location_detail(location_object_id: str):
    return await MongoLocationDetailRepository().get_location_detail_by_location_object_id(location_object_id)

@router.put("/api/physical_layer/locations_detail/{location_object_id}", response_model=LocationDetail)
async def update_location_detail(location_object_id: str, location_detail: LocationDetail):
    return await MongoLocationDetailRepository().update_location_detail(location_object_id, location_detail)

@router.delete("/api/physical_layer/locations_detail/{location_object_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location_detail(location_object_id: str):
    return await MongoLocationDetailRepository().delete_location_detail(location_object_id)

@router.get("/api/physical_layer/locations_detail/{location_type}/locations_list", response_model=List[LocationDetail], response_model_exclude_unset=True)
async def get_locations_by_type(location_type: str):
    return await MongoLocationDetailRepository().get_location_detail_by_location_type(location_type)

@router.get("/api/physical_layer/locations_detail/{building_name}/building_plans", response_model=List[LocationDetail], response_model_exclude_unset=True)
async def get_building_plans(building_name: str):
    return await MongoLocationDetailRepository().get_locations_detail_by_building_id(building_name)

