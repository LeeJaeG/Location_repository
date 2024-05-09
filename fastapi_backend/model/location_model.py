from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4



class Rack(BaseModel):
    rack_name: Optional[str] = None
    rack_id: UUID = Field(default_factory=uuid4, unique=True)
    devices: Optional[List[str]] = None  # Changed Devices to Device


class Room(BaseModel):
    room_name: Optional[str] = None
    room_id: UUID = Field(default_factory=uuid4, unique=True)
    racks: Optional[List[Rack]] = None  # Changed Racks to Rack
    devices: Optional[List[str]] = None  # Changed Devices to Device

class Floor(BaseModel):
    floor_name: Optional[str] = None
    floor_id: UUID = Field(default_factory=uuid4, unique=True)
    rooms: Optional[List[Room]] = None  # Changed Rooms to Room
    racks: Optional[List[Rack]] = None  # Changed Racks to Rack
    devices: Optional[List[str]] = None  # Changed Devices to Device

class Location(BaseModel):
    building_id: UUID = Field(default_factory=uuid4, unique=True)  # Changed UUID to ObjectId
    building_name: Optional[str] = None
    building_address: Optional[str] = None
    floors: Optional[List[Floor]] = None  # Changed Floors to Floor
    racks: Optional[List[Rack]] = None  # Changed Racks to Rack
    devices: Optional[List[str]] = None  # Changed Devices to Device
    rooms: Optional[List[Room]] = None  # Changed Rooms to Room
    
    model_config={
        "json_schema_extra" : {
            "examples": [{
                "building_name": "Main HQ",
                "building_address": "1234 Main St",
                "floors": [
                    {
                        "floor_name": "First Floor",
                        "rooms": [
                            {
                                "room_name": "Server Room",
                                "racks": [
                                    {
                                        "rack_name": "Rack 101",
                                        "devices": [
                                            "11111111-2222-3333-4444-555555555555"  # Changed to dictionary format
                                        ]   
                                    }
                                ]
                            }
                        ],
                        "devices": [
                            "11111111-2222-3333-4444-555555555555"  # Changed to dictionary format
                        ]
                    }
                ],
                "racks": [
                    {
                        "rack_name": "Rack 201",
                        "devices": [
                            "11111111-2222-3333-4444-555555555555"  # Changed to dictionary format
                        ]
                    }
                ],
                "devices": [
                    "11111111-2222-3333-4444-555555555555"  # Changed to dictionary format
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
            building_address=self.building_address,  # Set building address if available
            location_path=f"/{self.building_id}"
        )
        location_details.append(building_detail)
        if self.racks:
            for rack in self.racks:
                rack_detail = LocationDetail(
                    location_object_id=str(rack.rack_id),
                    location_type="rack",
                    location_path=f"/{self.building_id}/0/0/{rack.rack_id}",
                    location_parent_id=str(self.building_id)
                )
                location_details.append(rack_detail)
         
        if self.rooms:
            for room in self.rooms:
                room_detail = LocationDetail(
                    location_object_id=str(room.room_id),
                    location_type="room",
                    location_path=f"/{self.building_id}/0/{room.room_id}",
                    location_parent_id=str(self.building_id)
                )
                location_details.append(room_detail)
                if room.racks:
                    for rack in room.racks:
                        rack_detail = LocationDetail(
                        location_object_id=str(rack.rack_id),
                        location_type="rack",
                        location_path=f"/{self.building_id}/0/{room.room_id}/{rack.rack_id}",
                        location_parent_id=str(room.room_id)
                    )
                    location_details.append(rack_detail)
        # Create LocationDetail for floors
        if self.floors:
            for floor in self.floors:
                floor_detail = LocationDetail(
                    location_object_id=str(floor.floor_id),
                    location_type="floor",
                    location_path=f"/{self.building_id}/{floor.floor_id}",
                    location_parent_id=str(self.building_id)
                )
                location_details.append(floor_detail)
            if floor.racks:
                for rack in floor.racks:
                    rack_detail = LocationDetail(
                    location_object_id=str(rack.rack_id),
                    location_type="rack",
                    location_path=f"/{self.building_id}/{floor.floor_id}/0/{rack.rack_id}",
                    location_parent_id=str(floor.floor_id)
                )
                location_details.append(rack_detail)
        
            # Create LocationDetail for rooms
            if floor.rooms:
                for room in floor.rooms:
                    room_detail = LocationDetail(
                        location_object_id=str(room.room_id),
                        location_type="room",
                        location_path=f"/{self.building_id}/{floor.floor_id}/{room.room_id}",
                        location_parent_id=str(floor.floor_id)
                    )
                    location_details.append(room_detail)

                # Create LocationDetail for racks
                if room.racks:
                    for rack in room.racks:
                        rack_detail = LocationDetail(
                        location_object_id=str(rack.rack_id),
                        location_type="rack",
                        location_path=f"/{self.building_id}/{floor.floor_id}/{room.room_id}/{rack.rack_id}",
                        location_parent_id=str(room.room_id)
                    )
                    location_details.append(rack_detail)

        return location_details
    
class LocationResponse(Location):
    model_config={
        "json_schema_extra" : {
            "examples": [{
                "building_id": "550e8400-e29b-41d4-a716-446655440000",
                "building_name": "Main HQ",
                "building_address": "1234 Main St",
                "floors": [
                    {
                        "floor_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                        "floor_name": "First Floor",
                        "rooms": [
                            {
                                "room_id": "f44d0e18-8b12-4d0e-9121-a6d6d0b8f2e6",
                                "room_name": "Server Room",
                                "racks": [
                                    {
                                        "rack_id": "a8b1c2d3-e4f5-67g8-90h1-i2j3k4l5m6n7",
                                        "rack_name": "Rack 101",
                                        "devices": [
                                            "11111111-2222-3333-4444-555555555555"  # Changed to dictionary format
                                        ]   
                                    }
                                ]
                            }
                        ],
                        "devices": [
                            "11111111-2222-3333-4444-555555555555"  # Changed to dictionary format
                        ]
                    }
                ],
                "racks": [
                    {
                        "rack_id": "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6",
                        "rack_name": "Rack 201",
                        "devices": [
                            "11111111-2222-3333-4444-555555555555"  # Changed to dictionary format
                        ]
                    }
                ],
                "devices": [
                    "11111111-2222-3333-4444-555555555555"  # Changed to dictionary format
                ]
            }]
        }
    }

