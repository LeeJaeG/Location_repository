from typing import List
from fastapi import HTTPException
from ..model.location_model import Location, LocationResponse
from ..db.database import MongoLocationRepository, MongoLocationDetailRepository

class LocationService:
    def __init__(self):
        self.location_repo = MongoLocationRepository()
        self.location_detail_repo = MongoLocationDetailRepository()

    async def get_all_locations(self) -> List[Location]:
        try:
            return await self.location_repo.get_all_locations()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to fetch locations")

    async def get_location_by_id(self, building_id: str) -> Location:
        try:
            location = await self.location_repo.get_location(building_id)
            if location is None:
                raise HTTPException(status_code=404, detail="Location not found")
            return location
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="Server error")

    async def create_location(self, building: Location) -> LocationResponse:
        try:
            location = await self.location_repo.create_location(building)
            for detail in building.create_location_details():
                await self.location_detail_repo.create_location_detail(detail)
            return location
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to create location")

    async def update_location(self, building_id: str, building: Location) -> Location:
        try:
            await self.location_repo.delete_location(building_id)
            return await self.location_repo.create_location(building)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to update location")

    async def delete_location(self, building_id: str):
        try:
            return await self.location_repo.delete_location(building_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to delete location")
        
location_service = LocationService()