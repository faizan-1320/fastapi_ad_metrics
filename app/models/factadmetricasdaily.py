from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

# Dimension Tables
class DimDate(Base):
    __tablename__ = "dim_date"
    date_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_value = Column(String(20), nullable=False)


class DimRegion(Base):
    __tablename__ = "dim_region"
    region_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region_name = Column(String(100), nullable=False)


class DimAgeGroup(Base):
    __tablename__ = "dim_age_group"
    age_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    age_range = Column(String(50), nullable=False)


class DimGender(Base):
    __tablename__ = "dim_gender"
    gender_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gender_name = Column(String(10), nullable=False)


class DimPlatform(Base):
    __tablename__ = "dim_platform"
    platform_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    platform_name = Column(String(50), nullable=False)


class DimPlacement(Base):
    __tablename__ = "dim_placement"
    placement_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    placement_name = Column(String(50), nullable=False)


class DimDeviceType(Base):
    __tablename__ = "dim_device_type"
    device_type_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_type_name = Column(String(50), nullable=False)


# Fact Table with relationships
class FactAdMetricsDaily(Base):
    __tablename__ = 'fact_ad_metrics_daily'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_id = Column(Integer, ForeignKey("dim_date.date_id"))
    region_id = Column(Integer, ForeignKey("dim_region.region_id"))
    age_id = Column(Integer, ForeignKey("dim_age_group.age_id"))
    gender_id = Column(Integer, ForeignKey("dim_gender.gender_id"))
    platform_id = Column(Integer, ForeignKey("dim_platform.platform_id"))
    placement_id = Column(Integer, ForeignKey("dim_placement.placement_id"))
    device_type_id = Column(Integer, ForeignKey("dim_device_type.device_type_id"))
    impressions = Column(Integer)
    clicks = Column(Integer)
    cost = Column(Float)
    conversions = Column(Integer)
    likes = Column(Integer)

    # ✅ Relationships
    date = relationship("DimDate", backref="ad_metrics")
    region = relationship("DimRegion", backref="ad_metrics")
    age_group = relationship("DimAgeGroup", backref="ad_metrics")
    gender = relationship("DimGender", backref="ad_metrics")
    platform = relationship("DimPlatform", backref="ad_metrics")
    placement = relationship("DimPlacement", backref="ad_metrics")
    device_type = relationship("DimDeviceType", backref="ad_metrics")
