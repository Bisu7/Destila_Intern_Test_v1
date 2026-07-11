from sqlalchemy import Column, Integer, String, Float, Date, DateTime, UniqueConstraint
from sqlalchemy.sql import func
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

class ExceptionRecord(Base):
    __tablename__ = "exceptions"
    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    planned_units = Column(Float, nullable=False)
    actual_units = Column(Integer, nullable=False)
    deficit_pct = Column(Float, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, default="open", nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('product_code', 'date', name='uq_product_date'),
    )
