import time
import uuid
from fastapi import FastAPI, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import SessionLocal
from core.models import NormalizedData

app = FastAPI(title="Backend & ETL API")


@app.get("/health")
def health():
    try:
        session: Session = SessionLocal()
        session.execute(text("SELECT 1"))
        session.close()
        return {"status": "ok"}
    except Exception:
        return {"status": "ok","db":"unavailable"}


@app.get("/data")
def get_data(
    source: str | None = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    start_time = time.time()
    request_id = str(uuid.uuid4())

    session: Session = SessionLocal()
    query = session.query(NormalizedData)

    if source:
        query = query.filter(NormalizedData.source == source)

    total = query.count()
    records = query.offset(offset).limit(limit).all()
    session.close()

    latency_ms = int((time.time() - start_time) * 1000)

    return {
        "request_id": request_id,
        "latency_ms": latency_ms,
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": [
            {
                "record_id": r.record_id,
                "name": r.name,
                "value": r.value,
                "source": r.source,
            }
            for r in records
        ],
    }
