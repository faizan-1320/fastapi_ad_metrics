from pydantic import BaseModel, Field

class DateCreate(BaseModel):
    date_value: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Format: YYYY-MM-DD")

class RegionCreate(BaseModel):
    region_name: str = Field(..., pattern=r"^[A-Za-z ]+$", min_length=1, max_length=100)

class AgeGroupCreate(BaseModel):
    age_range: str = Field(..., pattern=r"^\d+$", min_length=1, max_length=3)

class GenderCreate(BaseModel):
    gender_name: str = Field(..., pattern=r"^[A-Za-z]+$", min_length=1, max_length=10)

class PlatformCreate(BaseModel):
    platform_name: str = Field(..., pattern=r"^[A-Za-z ]+$", min_length=1, max_length=50)

class PlacementCreate(BaseModel):
    placement_name: str = Field(..., pattern=r"^[A-Za-z ]+$", min_length=1, max_length=50)

class DeviceTypeCreate(BaseModel):
    device_type_name: str = Field(..., pattern=r"^[A-Za-z ]+$", min_length=1, max_length=50)