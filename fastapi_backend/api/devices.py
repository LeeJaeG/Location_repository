from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List
from ..model.device_model import Device

router = APIRouter()

@router.get("/devices", response_model=List[Device], response_model_exclude_unset=True)
async def read_devices():
    # 여기에 실제 디바이스 데이터를 조회하는 로직을 구현합니다.
    # 예시 데이터를 반환합니다.
    return [
        {
            "device_id": "1",
            "device_name": "Device 1",
            "location_path": "building1.floor1.room1.rack1",
            "location_parent_id": "rack1",
            "device_type_id": "type1",
            "sensor_type_id": "sensor1",
            "device_group_id": "group1",
            "device_role_id": "role1",
            "device_status": "active",
            "interface_id": "interface1",
            "x": 1.0,
            "y": 2.0
        }
    ]
