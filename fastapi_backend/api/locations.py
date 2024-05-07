from fastapi import APIRouter, HTTPException, Path, Query, Body, status
from typing import List, Optional
from ..model.location_model import Location, LocationDetail
from ..db.database import MongoLocationRepository, MongoLocationDetailRepository

router = APIRouter()

# Locations
@router.get("/api/physical_layer/locations", response_model=List[Location], response_model_exclude_unset=True)
async def get_locations():
    """
    Retrieve all locations from the database.
    Returns a list of Location objects.
    """
    try:
        locations = await MongoLocationRepository().get_all_locations()
        return locations
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch locations")

@router.get("/api/physical_layer/locations/{building_id}", response_model=Location, response_model_exclude_unset=True)
async def get_location_by_id(building_id: str):
    """
    Retrieve a specific location by its ID.
    Parameters:
        - location_id: str - The unique identifier for the location.
    Returns a single Location object or a 404 error if not found.
    """
    try:
        location = await MongoLocationRepository().get_location(building_id)
        if location is None:
            raise HTTPException(status_code=404, detail="Location not found")
        return location
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")

@router.put("/api/physical_layer/locations/{building_id}", response_model=Location, response_model_exclude_unset=True)
async def update_location(building_id: str, building: Location):
    """
    Update an existing location.
    Parameters:
        - building_id: str - The unique identifier for the location to update.
        - building: Location - The updated location object.
    Returns the updated Location object.
    """
    try :
        await MongoLocationRepository().delete_location(building_id)
        return await MongoLocationRepository().create_location(building)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update location")

@router.delete("/api/physical_layer/locations/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(building_id: str):
    """
    Delete a location by its ID.
    Parameters:
        - building_id: str - The unique identifier for the location to delete.
    Returns a 204 No Content response on successful deletion.
    """
    try :
        return await MongoLocationRepository().delete_location(building_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete location")

@router.post("/api/physical_layer/locations", response_model=Location)
async def create_location(building: Location):
    """
    Create a new location.
    Parameters:
        - building: Location - The location object to create.
    Returns the newly created Location object.
    """
    try:
        location = await MongoLocationRepository().create_location(building)
        for detail in building.create_location_details():
            await MongoLocationDetailRepository().create_location_detail(detail)
        return location
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to create location", headers={"X-Error": str(e)})
