from fastapi import APIRouter,Depends,HTTPException
from app.schemas.factadmetricasdaily import AdMetricFilter,FactAdMetricsCreate
from sqlalchemy.orm import Session
from app.crud.crud import get_ad_metrics,create_ad_metric
from app.database import get_db

router =APIRouter()

@router.post("/metrics/")
def post_metrics(data: FactAdMetricsCreate, db: Session = Depends(get_db)):
    try:
        return create_ad_metric(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metrics")
def read_metrics(filters: AdMetricFilter = Depends(), db: Session = Depends(get_db)):
    try:
        return get_ad_metrics(db, filters)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))