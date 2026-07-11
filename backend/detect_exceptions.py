import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, engine, Base
from backend.models import ProductionPlan, ActualProduction, ExceptionRecord

def detect_exceptions():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # We choose to SKIP plan rows that have no matching actuals because our actuals
    # data only runs up to Q1. Treating missing actuals as 0 would flag 9 months of
    # future plans as exceptions, which is noise, not a true production failure.
    
    try:
        plans = db.query(ProductionPlan).all()
        actuals = db.query(ActualProduction).all()
        
        actuals_dict = {(a.product_code, a.date): a.units_produced for a in actuals}
        
        for plan in plans:
            key = (plan.product_code, plan.date)
            if key not in actuals_dict:
                continue 
            
            actual_units = actuals_dict[key]
            planned_units = plan.planned_units
            
            if actual_units < 0.9 * planned_units:
                severity = "high" if actual_units < 0.7 * planned_units else "medium"
                deficit_pct = (planned_units - actual_units) / planned_units
                
                existing = db.query(ExceptionRecord).filter(
                    ExceptionRecord.product_code == plan.product_code,
                    ExceptionRecord.date == plan.date
                ).first()
                
                if existing:
                    existing.planned_units = planned_units
                    existing.actual_units = actual_units
                    existing.deficit_pct = deficit_pct
                    existing.severity = severity
                else:
                    new_exc = ExceptionRecord(
                        product_code=plan.product_code,
                        date=plan.date,
                        planned_units=planned_units,
                        actual_units=actual_units,
                        deficit_pct=deficit_pct,
                        severity=severity,
                        status="open"
                    )
                    db.add(new_exc)
        
        db.commit()
        
        high_count = db.query(ExceptionRecord).filter(ExceptionRecord.severity == "high").count()
        med_count = db.query(ExceptionRecord).filter(ExceptionRecord.severity == "medium").count()
        
        print("=== Exception Detection Summary ===")
        print(f"Total exceptions found: {high_count + med_count}")
        print(f"  - High severity: {high_count}")
        print(f"  - Medium severity: {med_count}")

    finally:
        db.close()

if __name__ == "__main__":
    detect_exceptions()
