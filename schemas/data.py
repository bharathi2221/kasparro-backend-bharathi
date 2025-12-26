from pydantic import BaseModel, Field
from typing import Optional


class APIRecord(BaseModel):
    record_id: str
    name: str
    value: str


class CSVRecord(BaseModel):
    record_id: str
    name: Optional[str]
    value: Optional[str]


class NormalizedRecord(BaseModel):
    record_id: str
    name: Optional[str]
    value: Optional[str]
    source: str
