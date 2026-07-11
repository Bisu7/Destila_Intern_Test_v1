from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import timedelta
from typing import List, Optional

from .database import get_db
from . import models, schemas

app = FastAPI(title="Mini Exception Inbox API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/exceptions", response_model=List[schemas.ExceptionResponse])
def get_exceptions(
    product_code: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List exceptions sorted by date and deficit percentage."""
    query = db.query(models.ExceptionRecord)
    
    if product_code:
        query = query.filter(models.ExceptionRecord.product_code == product_code)
    if severity:
        query = query.filter(models.ExceptionRecord.severity == severity)
        
    query = query.order_by(
        desc(models.ExceptionRecord.date),
        desc(models.ExceptionRecord.deficit_pct)
    )
    
    return query.all()

@app.get("/exceptions/{id}", response_model=schemas.ExceptionDetailResponse)
def get_exception_detail(id: int, db: Session = Depends(get_db)):
    """Get single exception details with a 7-day trailing trend."""
    exc = db.query(models.ExceptionRecord).filter(models.ExceptionRecord.id == id).first()
    if not exc:
        raise HTTPException(status_code=404, detail="Exception not found")
        
    start_date = exc.date - timedelta(days=6)
    
    plans = db.query(models.ProductionPlan).filter(
        models.ProductionPlan.product_code == exc.product_code,
        models.ProductionPlan.date >= start_date,
        models.ProductionPlan.date <= exc.date
    ).all()
    
    actuals = db.query(models.ActualProduction).filter(
        models.ActualProduction.product_code == exc.product_code,
        models.ActualProduction.date >= start_date,
        models.ActualProduction.date <= exc.date
    ).all()
    
    actuals_dict = {a.date: a.units_produced for a in actuals}
    
    trend = []
    for p in plans:
        trend.append({
            "date": p.date,
            "planned_units": p.planned_units,
            "actual_units": actuals_dict.get(p.date, 0)
        })
        
    trend.sort(key=lambda x: x["date"])
    
    resp_data = exc.__dict__.copy()
    resp_data["last_7_days"] = trend
    
    return resp_data

@app.patch("/exceptions/{id}", response_model=schemas.ExceptionResponse)
def update_exception(id: int, update_data: schemas.ExceptionUpdate, db: Session = Depends(get_db)):
    """Update exception status."""
    exc = db.query(models.ExceptionRecord).filter(models.ExceptionRecord.id == id).first()
    if not exc:
        raise HTTPException(status_code=404, detail="Exception not found")
        
    exc.status = update_data.status
    db.commit()
    db.refresh(exc)
    
    return exc
