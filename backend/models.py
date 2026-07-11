from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class RawProductionPlan(Base):
    __tablename__ = "raw_production_plan"
    id = Column(Integer, primary_key=True, index=True)
    plan_date = Column(String)
    plant = Column(String)
    sku = Column(String)
    planned_units = Column(Float, nullable=True)

class RawActualProduction(Base):
    __tablename__ = "raw_actual_production"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    plant_id = Column(String)
    product_code = Column(String)
    units_produced = Column(Integer)

class ProductionPlan(Base):
    __tablename__ = "production_plan"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    plant_id = Column(String)
    product_code = Column(String)
    planned_units = Column(Float)

class ActualProduction(Base):
    __tablename__ = "actual_production"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    plant_id = Column(String)
    product_code = Column(String)
    units_produced = Column(Integer)
