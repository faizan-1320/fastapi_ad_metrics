from fastapi import HTTPException
from sqlalchemy.orm import Session,joinedload
from sqlalchemy.exc import IntegrityError
from app.models import FactAdMetricsDaily,DimRegion,DimPlatform
from app.schemas.factadmetricasdaily import AdMetricFilter,FactAdMetricsCreate

def create_ad_metric(db: Session, data: FactAdMetricsCreate):
    from ..models import DimDate, DimRegion, DimAgeGroup, DimGender, DimPlatform, DimPlacement, DimDeviceType

    # 🔍 Manual FK checks
    if not db.query(DimDate).filter_by(date_id=data.date_id).first():
        raise HTTPException(status_code=404, detail="Date not found")
    if not db.query(DimRegion).filter_by(region_id=data.region_id).first():
        raise HTTPException(status_code=404, detail="Region not found")
    if not db.query(DimAgeGroup).filter_by(age_id=data.age_id).first():
        raise HTTPException(status_code=404, detail="Age group not found")
    if not db.query(DimGender).filter_by(gender_id=data.gender_id).first():
        raise HTTPException(status_code=404, detail="Gender not found")
    if not db.query(DimPlatform).filter_by(platform_id=data.platform_id).first():
        raise HTTPException(status_code=404, detail="Platform not found")
    if not db.query(DimPlacement).filter_by(placement_id=data.placement_id).first():
        raise HTTPException(status_code=404, detail="Placement not found")
    if not db.query(DimDeviceType).filter_by(device_type_id=data.device_type_id).first():
        raise HTTPException(status_code=404, detail="Device type not found")

    record = FactAdMetricsDaily(**data.dict())
    db.add(record)
    try:
        db.commit()
        db.refresh(record)
        return record
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Unable to insert ad metric due to constraint error.")

def get_ad_metrics(db: Session, filters: AdMetricFilter):
    from ..models import (
        FactAdMetricsDaily,
        DimDate,
        DimRegion, DimAgeGroup, DimGender,
        DimPlatform, DimPlacement, DimDeviceType
    )

    # Step 1: Resolve flexible start/end date_ids
    start_date_obj = db.query(DimDate).filter(DimDate.date_value >= filters.start_date).order_by(DimDate.date_value.asc()).first()
    end_date_obj = db.query(DimDate).filter(DimDate.date_value <= filters.end_date).order_by(DimDate.date_value.desc()).first()

    if not start_date_obj or not end_date_obj:
        raise HTTPException(status_code=404, detail="Start or end date not found near the given range")

    # Step 2: Build base query with date filter
    query = db.query(FactAdMetricsDaily).filter(
        FactAdMetricsDaily.date_id >= start_date_obj.date_id,
        FactAdMetricsDaily.date_id <= end_date_obj.date_id,
    )

    # Step 3: Apply all other filters
    if filters.region:
        region = db.query(DimRegion).filter(DimRegion.region_name.ilike(f"%{filters.region}%")).first()
        if not region:
            raise HTTPException(status_code=404, detail=f"No region like '{filters.region}' found")
        query = query.filter(FactAdMetricsDaily.region_id == region.region_id)

    if filters.age_group:
        age = db.query(DimAgeGroup).filter(DimAgeGroup.age_range.ilike(f"%{filters.age_group}%")).first()
        if not age:
            raise HTTPException(status_code=404, detail=f"No age group like '{filters.age_group}' found")
        query = query.filter(FactAdMetricsDaily.age_id == age.age_id)

    if filters.gender:
        gender = db.query(DimGender).filter(DimGender.gender_name.ilike(f"%{filters.gender}%")).first()
        if not gender:
            raise HTTPException(status_code=404, detail=f"No gender like '{filters.gender}' found")
        query = query.filter(FactAdMetricsDaily.gender_id == gender.gender_id)

    if filters.platform:
        platform = db.query(DimPlatform).filter(DimPlatform.platform_name.ilike(f"%{filters.platform}%")).first()
        if not platform:
            raise HTTPException(status_code=404, detail=f"No platform like '{filters.platform}' found")
        query = query.filter(FactAdMetricsDaily.platform_id == platform.platform_id)

    if filters.placement:
        placement = db.query(DimPlacement).filter(DimPlacement.placement_name.ilike(f"%{filters.placement}%")).first()
        if not placement:
            raise HTTPException(status_code=404, detail=f"No placement like '{filters.placement}' found")
        query = query.filter(FactAdMetricsDaily.placement_id == placement.placement_id)

    if filters.device_type:
        device = db.query(DimDeviceType).filter(DimDeviceType.device_type_name.ilike(f"%{filters.device_type}%")).first()
        if not device:
            raise HTTPException(status_code=404, detail=f"No device type like '{filters.device_type}' found")
        query = query.filter(FactAdMetricsDaily.device_type_id == device.device_type_id)

    if filters.impressions is not None:
        query = query.filter(FactAdMetricsDaily.impressions == filters.impressions)
    if filters.clicks is not None:
        query = query.filter(FactAdMetricsDaily.clicks == filters.clicks)
    if filters.cost is not None:
        query = query.filter(FactAdMetricsDaily.cost == filters.cost)
    if filters.conversions is not None:
        query = query.filter(FactAdMetricsDaily.conversions == filters.conversions)
    if filters.likes is not None:
        query = query.filter(FactAdMetricsDaily.likes == filters.likes)

    # Step 4: Load related tables with joinedload
    query = query.options(
        joinedload(FactAdMetricsDaily.date),
        joinedload(FactAdMetricsDaily.region),
        joinedload(FactAdMetricsDaily.age_group),
        joinedload(FactAdMetricsDaily.gender),
        joinedload(FactAdMetricsDaily.platform),
        joinedload(FactAdMetricsDaily.placement),
        joinedload(FactAdMetricsDaily.device_type),
    )

    result = query.all()
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No ad metrics found for the given filters."
        )
    # Step 5: Format response
    response = []
    for row in result:
        response.append({
            "date": row.date.date_value,
            "region": row.region.region_name,
            "age": row.age_group.age_range,
            "gender": row.gender.gender_name,
            "platform": row.platform.platform_name,
            "placement": row.placement.placement_name,
            "device_type": row.device_type.device_type_name,
            "impressions": row.impressions,
            "clicks": row.clicks,
            "cost": row.cost,
            "conversions": row.conversions,
            "likes": row.likes,
        })

    return response

