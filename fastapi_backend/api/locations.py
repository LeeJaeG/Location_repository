from fastapi import APIRouter, status
from typing import List
from ..model.location_model import Location, LocationResponse
from ..service.location_service import location_service

router = APIRouter()

# Locations
@router.get("/api/physical_layer/locations", response_model=List[Location], response_model_exclude_unset=True)
async def get_locations():
    """
    Retrieve all locations from the database.
    Returns a list of Location objects.
    """
    return await location_service.get_all_locations()

@router.get("/api/physical_layer/locations/{building_id}", response_model=Location, response_model_exclude_unset=True)
async def get_location_by_id(building_id: str):
    """
    Retrieve a specific location by its ID.
    Parameters:
        - location_id: str - The unique identifier for the location.
    Returns a single Location object or a 404 error if not found.
    """
    return await location_service.get_location_by_id(building_id)

@router.put("/api/physical_layer/locations/{building_id}", response_model=Location, response_model_exclude_unset=True)
async def update_location(building_id: str, building: Location):
    """
    Update an existing location.
    Parameters:
        - building_id: str - The unique identifier for the location to update.
        - building: Location - The updated location object.
    Returns the updated Location object.
    """
    return await location_service.update_location(building_id, building)

@router.delete("/api/physical_layer/locations/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(building_id: str):
    """
    Delete a location by its ID.
    Parameters:
        - building_id: str - The unique identifier for the location to delete.
    Returns a 204 No Content response on successful deletion.
    """
    return await location_service.delete_location(building_id)

@router.post("/api/physical_layer/locations", response_model=LocationResponse)
async def create_location(building: Location):
    """
    Create a new location.
    Parameters:
        - building: Location - The location object to create.
    Returns the newly created Location object.
    """
    print(building)
    return await location_service.create_location(building)
