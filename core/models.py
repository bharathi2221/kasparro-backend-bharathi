from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from core.database import Base


class RawAPIData(Base):
    __tablename__ = "raw_api_data"

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())


class RawCSVData(Base):
    __tablename__ = "raw_csv_data"

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())


class NormalizedData(Base):
    __tablename__ = "normalized_data"

    id = Column(Integer, primary_key=True)
    record_id = Column(String, nullable=False)
    name = Column(String)
    value = Column(String)
    source = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoints"

    id = Column(Integer, primary_key=True)
    source = Column(String, unique=True, nullable=False)
    last_run_at = Column(DateTime(timezone=True), server_default=func.now())
