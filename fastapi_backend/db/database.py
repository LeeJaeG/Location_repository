from motor.motor_asyncio import AsyncIOMotorClient
from abc import ABC, abstractmethod
from typing import List, Optional
from ..model.location_model import Location
from ..model.locationDetail_model import LocationDetail
from ..model.device_model import Device
from bson.codec_options import CodecOptions, UuidRepresentation
from uuid import UUID
from ..core.settings import settings

DATABASE_URL = settings.mongo_url
DB_NAME = settings.mongo_db
client = AsyncIOMotorClient(DATABASE_URL)
db = client[DB_NAME]

class LocationRepository(ABC):
    def __init__(self):
        super().__init__()
        self.collection = db.get_collection("location_collection", codec_options=CodecOptions(uuid_representation=UuidRepresentation.STANDARD))

    @abstractmethod
    async def create_location(self, location: Location) -> Location:
        pass

    @abstractmethod
    async def get_location(self, location_id: str) -> Optional[Location]:
        pass

    @abstractmethod
    async def get_all_locations(self) -> List[Location]:
        pass

class LocationDetailRepository(ABC):
    def __init__(self):
        super().__init__()
        self.collection = db.get_collection("location_detail_collection", codec_options=CodecOptions(uuid_representation=UuidRepresentation.STANDARD))

    @abstractmethod
    async def create_location_detail(self, detail: LocationDetail) -> LocationDetail:
        pass

    @abstractmethod
    async def get_location_detail(self, detail_id: str) -> Optional[LocationDetail]:
        pass
    
    @abstractmethod
    async def get_location_detail_by_location_object_id(self, location_object_id: str) -> Optional[LocationDetail]:
        pass
    
    @abstractmethod
    async def get_location_detail_by_location_type(self, location_type: str) -> Optional[List[LocationDetail]]:
        pass
    
    @abstractmethod
    async def get_locations_detail_by_building_id(self, building_id: str) -> Optional[List[LocationDetail]]:
        pass

class DeviceRepository(ABC):
    def __init__(self):
        super().__init__()
        self.collection = db.get_collection("device_collection", codec_options=CodecOptions(uuid_representation=UuidRepresentation.STANDARD))

    @abstractmethod
    async def create_device(self, device: Device) -> Device:
        pass

    @abstractmethod
    async def get_device(self, device_id: str) -> Optional[Device]:
        pass

class MongoLocationRepository(LocationRepository):
    async def create_location(self, location: Location) -> Location:
        try:
            # print(location.model_dump(exclude_none=True).pop("building_address"))
            await self.collection.insert_one(location.model_dump(exclude_none=True))
            return location
        except Exception as e:
            raise e

    async def get_location(self, building_id: str) -> Optional[Location]:
        try:
            data = await self.collection.find_one({"building_id": UUID(building_id)})
            return Location(**data) if data else None
        except Exception as e:
            raise e

    async def get_all_locations(self) -> List[Location]:
        try:
            locations = await self.collection.find().to_list(None)
            return [Location(**loc) for loc in locations]
        except Exception as e:
            raise e
        
    async def delete_location(self, building_id: str) -> bool:
        try:
            await self.collection.delete_one({"building_id": UUID(building_id)})
            return True
        except Exception as e:
            raise e

class MongoLocationDetailRepository(LocationDetailRepository):
    async def create_location_detail(self, detail: LocationDetail) -> LocationDetail:
        try:
            await self.collection.insert_one(detail.model_dump(exclude_none=True))
            return detail
        except Exception as e:
            raise e

    async def get_location_detail(self, detail_id: str) -> Optional[LocationDetail]:
        try:
            data = await self.collection.find_one({"id": detail_id})
            return LocationDetail(**data) if data else None
        except Exception as e:
            raise e

    async def get_location_detail_by_location_object_id(self, location_object_id: str) -> Optional[LocationDetail]:
        try:
            data = await self.collection.find_one({"location_object_id": location_object_id})
            return LocationDetail(**data) if data else None
        except Exception as e:
            raise e
        
    async def get_location_detail_by_location_type(self, location_type: str) -> Optional[List[LocationDetail]]:
        try:
            data = await self.collection.find({"location_type": location_type}).to_list(None)
            return [LocationDetail(**loc) for loc in data]
        except Exception as e:
            raise e

    async def get_locations_detail_by_building_id(self, building_id: str) -> Optional[List[LocationDetail]]:
        try:
            data = await self.collection.find({ "location_path": { "$regex": f".*{building_id}.*" } }).to_list(None)
            return data
        except Exception as e:
            raise e   
    
    async def delete_location_detail(self, detail_id: str) -> bool:
        try:
            await self.collection.delete_one({"id": detail_id})
            return True
        except Exception as e:
            raise e
    
    async def update_location_detail(self, detail_id: str, detail: LocationDetail) -> LocationDetail:
        try:
            await self.collection.update_one({"id": detail_id}, {"$set": detail.model_dump(exclude_none=True)})
            return detail
        except Exception as e:
            raise e

class MongoDeviceRepository(DeviceRepository):
    async def create_device(self, device: Device) -> Device:
        try:
            await self.collection.insert_one(device.model_dump(exclude_none=True))
            return device
        except Exception as e:
            raise e

    async def get_device(self, device_id: str) -> Optional[Device]:
        try:
            data = await self.collection.find_one({"id": device_id})
            return Device(**data) if data else None
        except Exception as e:
            raise e
