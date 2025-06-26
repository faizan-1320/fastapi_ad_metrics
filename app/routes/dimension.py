from fastapi import APIRouter,Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import (
    DateCreate, RegionCreate, AgeGroupCreate, GenderCreate,
    PlatformCreate, PlacementCreate, DeviceTypeCreate
)
from app.crud import (
    create_dim_date, create_dim_region, create_dim_age_group, create_dim_gender,
    create_dim_platform, create_dim_placement, create_dim_device_type
)

router = APIRouter()

@router.post("/date/")
def add_date(data: DateCreate, db: Session = Depends(get_db)):
    return create_dim_date(db, data)

@router.post("/region/")
def add_region(data: RegionCreate, db: Session = Depends(get_db)):
    return create_dim_region(db, data)

@router.post("/age-group/")
def add_age_group(data: AgeGroupCreate, db: Session = Depends(get_db)):
    return create_dim_age_group(db, data)

@router.post("/gender/")
def add_gender(data: GenderCreate, db: Session = Depends(get_db)):
    return create_dim_gender(db, data)

@router.post("/platform/")
def add_platform(data: PlatformCreate, db: Session = Depends(get_db)):
    return create_dim_platform(db, data)

@router.post("/placement/")
def add_placement(data: PlacementCreate, db: Session = Depends(get_db)):
    return create_dim_placement(db, data)

@router.post("/device-type/")
def add_device_type(data: DeviceTypeCreate, db: Session = Depends(get_db)):
    return create_dim_device_type(db, data)
