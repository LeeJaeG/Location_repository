from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Device(BaseModel):  # Changed class name from Devices to Device
    device_id: List[str]  # Changed from List[str] to str

class Rack(BaseModel):
    rack_name: Optional[str] = None
    rack_id: UUID = Field(default_factory=uuid4, unique=True)
    devices: Optional[List[Device]] = None  # Changed Devices to Device


class Room(BaseModel):
    room_name: Optional[str] = None
    room_id: UUID = Field(default_factory=uuid4, unique=True)
    racks: Optional[List[Rack]] = None  # Changed Racks to Rack
    devices: Optional[List[Device]] = None  # Changed Devices to Device

class Floor(BaseModel):
    floor_name: Optional[str] = None
    floor_id: UUID = Field(default_factory=uuid4, unique=True)
    rooms: Optional[List[Room]] = None  # Changed Rooms to Room
    racks: Optional[List[Rack]] = None  # Changed Racks to Rack
    devices: Optional[List[Device]] = None  # Changed Devices to Device

class Location(BaseModel):
    building_id: UUID = Field(default_factory=uuid4, unique=True)  # Changed UUID to ObjectId
    building_name: Optional[str] = None
    floors: Optional[List[Floor]] = None  # Changed Floors to Floor
    racks: Optional[List[Rack]] = None  # Changed Racks to Rack
    devices: Optional[List[Device]] = None  # Changed Devices to Device
    rooms: Optional[List[Room]] = None  # Changed Rooms to Room
    
    model_config={
        "json_schema_extra" : {
            "examples": [{
                "building_id": "B1",
                "building_name": "Main HQ",
                "floors": [
                    {
                        "floor_name": "First Floor",
                        "floor_id": "F1",
                        "rooms": [
                            {
                                "room_name": "Server Room",
                                "room_id": "R1",
                                "racks": [
                                    {
                                        "rack_name": "Rack 101",
                                        "rack_id": "RK1",
                                        "devices": [
                                            {"device_id": "D1"}  # Changed to dictionary format
                                        ]   
                                    }
                                ]
                            }
                        ],
                        "devices": [
                            {"device_id": "D1"}  # Changed to dictionary format
                        ]
                    }
                ],
                "racks": [
                    {
                        "rack_name": "Rack 201",
                        "rack_id": "RK2",
                        "devices": [
                            {"device_id": "D1"}  # Changed to dictionary format
                        ]
                    }
                ],
                "devices": [
                    {"device_id": "D1"}  # Changed to dictionary format
                ]
            }]
        }
    }
    def create_location_details(self):
        location_details = []

        # Create LocationDetail for building
        building_detail = LocationDetail(
            location_object_id=str(self.building_id),
            location_type="building",
            building_address=None,  # Set building address if available
            location_path=f"/{self.building_name}"
        )
        location_details.append(building_detail)
        if self.racks:
            for rack in self.racks:
                rack_detail = LocationDetail(
                    location_object_id=str(rack.rack_id),
                    location_type="rack",
                    location_path=f"/{self.building_name}/0/0/{rack.rack_name}",
                    location_parent_id=str(self.building_id)
                )
                location_details.append(rack_detail)
         
        if self.rooms:
            for room in self.rooms:
                room_detail = LocationDetail(
                    location_object_id=str(room.room_id),
                    location_type="room",
                    location_path=f"/{self.building_name}/0/{room.room_name}",
                    location_parent_id=str(self.building_id)
                )
                location_details.append(room_detail)
                if room.racks:
                    for rack in room.racks:
                        rack_detail = LocationDetail(
                        location_object_id=str(rack.rack_id),
                        location_type="rack",
                        location_path=f"/{self.building_name}/0/{room.room_name}/{rack.rack_name}",
                        location_parent_id=str(room.room_id)
                    )
                    location_details.append(rack_detail)
        # Create LocationDetail for floors
        if self.floors:
            for floor in self.floors:
                floor_detail = LocationDetail(
                    location_object_id=str(floor.floor_id),
                    location_type="floor",
                    location_path=f"/{self.building_name}/{floor.floor_name}",
                    location_parent_id=str(self.building_id)
                )
                location_details.append(floor_detail)
            if floor.racks:
                for rack in floor.racks:
                    rack_detail = LocationDetail(
                    location_object_id=str(rack.rack_id),
                    location_type="rack",
                    location_path=f"/{self.building_name}/{floor.floor_name}/0/{rack.rack_name}",
                    location_parent_id=str(floor.floor_id)
                )
                location_details.append(rack_detail)
        
            # Create LocationDetail for rooms
            if floor.rooms:
                for room in floor.rooms:
                    room_detail = LocationDetail(
                        location_object_id=str(room.room_id),
                        location_type="room",
                        location_path=f"/{self.building_name}/{floor.floor_name}/{room.room_name}",
                        location_parent_id=str(floor.floor_id)
                    )
                    location_details.append(room_detail)

                # Create LocationDetail for racks
                if room.racks:
                    for rack in room.racks:
                        rack_detail = LocationDetail(
                        location_object_id=str(rack.rack_id),
                        location_type="rack",
                        location_path=f"/{self.building_name}/{floor.floor_name}/{room.room_name}/{rack.rack_name}",
                        location_parent_id=str(room.room_id)
                    )
                    location_details.append(rack_detail)

        return location_details

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

