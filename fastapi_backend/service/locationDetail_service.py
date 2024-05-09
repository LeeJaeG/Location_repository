from typing import List
from fastapi import HTTPException
from ..model.locationDetail_model import LocationDetail
from ..db.database import MongoLocationDetailRepository

class LocationDetailService:
    def __init__(self):
        self.location_detail_repo = MongoLocationDetailRepository()

    async def get_location_detail(self, location_object_id: str) -> LocationDetail:
        try:
            location_detail = await self.location_detail_repo.get_location_detail_by_location_object_id(location_object_id)
            if location_detail is None:
                raise HTTPException(status_code=404, detail="Location detail not found")
            return location_detail
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="Server error")

    async def update_location_detail(self, location_object_id: str, location_detail: LocationDetail) -> LocationDetail:
        try:
            updated_location_detail = await self.location_detail_repo.update_location_detail(location_object_id, location_detail)
            if updated_location_detail is None:
                raise HTTPException(status_code=404, detail="Location detail not found")
            return updated_location_detail
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to update location detail")

    async def delete_location_detail(self, location_object_id: str):
        try:
            deleted = await self.location_detail_repo.delete_location_detail(location_object_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="Location detail not found")
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to delete location detail")

    async def get_locations_by_type(self, location_type: str) -> List[LocationDetail]:
        try:
            location_details = await self.location_detail_repo.get_location_detail_by_location_type(location_type)
            return location_details
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to fetch location details by type")

    async def get_building_plans(self, building_id: str) -> dict[str, List[LocationDetail]]:
        try:
            location_details_dict = {"building": [], "floor": [], "room": [], "rack": []}
            location_details = await self.location_detail_repo.get_locations_detail_by_building_id(building_id)
            for location in location_details:
                if location["location_type"] == "floor":
                    location_details_dict["floor"].append(location)
                elif location["location_type"] == "room":
                    location_details_dict["room"].append(location)
                elif location["location_type"] == "rack":
                    location_details_dict["rack"].append(location)
                else:
                    location_details_dict["building"].append(location)
            return location_details_dict
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Failed to fetch location details by type")

location_detail_service = LocationDetailService()