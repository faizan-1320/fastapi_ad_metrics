from app import models
from sqlalchemy.orm import Session

def create_dim_date(db: Session, data):
    record = models.DimDate(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def create_dim_region(db: Session, data):
    record = models.DimRegion(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def create_dim_age_group(db: Session, data):
    record = models.DimAgeGroup(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def create_dim_gender(db: Session, data):
    record = models.DimGender(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def create_dim_platform(db: Session, data):
    record = models.DimPlatform(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def create_dim_placement(db: Session, data):
    record = models.DimPlacement(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def create_dim_device_type(db: Session, data):
    record = models.DimDeviceType(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
