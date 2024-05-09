from fastapi import APIRouter, status
from typing import List
from ..model.locationDetail_model import LocationDetail
from ..service.locationDetail_service import location_detail_service

router = APIRouter()


@router.get("/api/physical_layer/locations_detail/{location_object_id}", response_model=LocationDetail, response_model_exclude_unset=True)
async def get_location_detail(location_object_id: str):
    """
    Retrieve a specific location detail by its object ID.
    Parameters:
        - location_object_id: str - The unique identifier for the location detail.
    Returns a single LocationDetail object or a 404 error if not found.
    """
    return await location_detail_service.get_location_detail(location_object_id)

@router.put("/api/physical_layer/locations_detail/{location_object_id}", response_model=LocationDetail)
async def update_location_detail(location_object_id: str, location_detail: LocationDetail):
    """
    Update an existing location detail.
    Parameters:
        - location_object_id: str - The unique identifier for the location detail to update.
        - location_detail: LocationDetail - The updated location detail object.
    Returns the updated LocationDetail object.
    """
    return await location_detail_service.update_location_detail(location_object_id, location_detail)

@router.delete("/api/physical_layer/locations_detail/{location_object_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location_detail(location_object_id: str):
    """
    Delete a location detail by its object ID.
    Parameters:
        - location_object_id: str - The unique identifier for the location detail to delete.
    Returns a 204 No Content response on successful deletion.
    """
    return await location_detail_service.delete_location_detail(location_object_id)

@router.get("/api/physical_layer/locations_detail/{location_type}/locations_list", response_model=List[LocationDetail], response_model_exclude_unset=True)
async def get_locations_by_type(location_type: str):
    """
    Retrieve a list of location details by location type.
    Parameters:
        - location_type: str - The type of location to filter by.
    Returns a list of LocationDetail objects matching the specified location type.
    """
    return await location_detail_service.get_locations_by_type(location_type)

@router.get("/api/physical_layer/locations_detail/{building_id}/building_plans", response_model=dict[str, List[LocationDetail]], response_model_exclude_unset=True)
async def get_building_plans(building_id: str):
    """
    Retrieve a list of location details representing building plans for a specific building.
    Parameters:
        - building_name: str - The name of the building to retrieve plans for.
    Returns a list of LocationDetail objects representing the building plans.
    """
    return await location_detail_service.get_building_plans(building_id)
