from pydantic import BaseModel, Field

class Device(BaseModel):
    device_id: str
    device_name: str
    location_path: str
    location_parent_id: str
    device_type_id: str
    sensor_type_id: str
    device_group_id: str
    device_role_id: str
    device_status: str
    interface_id: str
    x: float
    y: float